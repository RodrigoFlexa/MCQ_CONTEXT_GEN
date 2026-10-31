"""Busca PT/EN e revisão de português brasileiro, sem alterar fontes originais."""
import re
from collections import Counter
from functools import lru_cache

POLICY = '''Escreva os textos destinados ao leitor em português brasileiro natural,
com linguajar técnico usado no Brasil. Prefira vazão, equipe, treinamento,
planejamento, controle e monitoramento. Gestão e gerenciamento são ambos válidos.
Não traduza termos técnicos mecanicamente: offloading, topside, subsea, pig e
siglas consolidadas podem ser mantidos quando pertinentes, com explicação quando
necessária. Use trocador de calor ou permutador de calor conforme o uso técnico.
Ao ler inglês, preserve mecanismo, negação, condições, unidades e sentido de termos
polissêmicos: flow, trip, head, upset e scale dependem do contexto. Não transforme
jurisdição estrangeira em requisito brasileiro. Evidências literais e nomes próprios
permanecem no idioma original nos auxiliares. Consultas en são intencionalmente em inglês.
'''

REGIONAL = {'caudal':'vazão','equipa':'equipe','planeamento':'planejamento',
            'controlo':'controle','monitorização':'monitoramento'}


@lru_cache(maxsize=1)
def _factory():
    from langdetect import DetectorFactory
    from langdetect.detector_factory import PROFILES_DIRECTORY
    factory=DetectorFactory();factory.load_profile(PROFILES_DIRECTORY);factory.set_seed(0)
    return factory


def detect_language(value):
    """Identificação estatística é metadado, nunca motivo isolado de exclusão."""
    if len(value.split()) < 12:
        return dict(language='und',confidence=0.0,method='insufficient_text')
    try:
        from langdetect.lang_detect_exception import LangDetectException
        factory=_factory()
    except ImportError:
        return dict(language='und',confidence=0.0,method='dependency_unavailable')
    # Perfis compartilhados somente para leitura; um detector novo por texto.
    try:
        detector=factory.create();detector.append(value[:12000]);ranked=detector.get_probabilities()
    except LangDetectException:
        return dict(language='und',confidence=0.0,method='undetermined')
    if not ranked:return dict(language='und',confidence=0.0,method='undetermined')
    return dict(language=ranked[0].lang,confidence=round(ranked[0].prob,4),method='langdetect_seed_0')


def lint_ptbr(value):
    issues=[]
    for word,preferred in REGIONAL.items():
        if re.search(r'\b'+re.escape(word)+r'\b',value,re.I):
            issues.append(f'Prefira {preferred!r} ao regionalismo {word!r} no texto brasileiro')
    signal=detect_language(value)
    if len(value.split())>=25 and signal['confidence']>=.98 and signal['language'] not in ('pt','und'):
        issues.append('Texto longo identificado em idioma diferente de português; revise a redação em PT-BR')
    return issues


def validate_pairs(data,limit):
    pairs=data.get('pares')
    if not isinstance(pairs,list) or not 1<=len(pairs)<=limit:
        raise ValueError('Entregue entre um e limite pares PT/EN')
    seen=set()
    for pair in pairs:
        if not isinstance(pair,dict) or set(pair)!={'pt','en'}:
            raise ValueError('Cada consulta precisa de pt e en explícitos')
        for lang in ('pt','en'):
            if not isinstance(pair[lang],str) or not 3<=len(pair[lang].split())<=40:
                raise ValueError('Consulta deve ter de 3 a 40 palavras')
            if re.search(r'[\x00-\x1f]',pair[lang]):raise ValueError('Consulta contém caracteres de controle')
            signal=detect_language(pair[lang])
            if signal['confidence']>=.98 and signal['language'] not in (lang,'und'):
                raise ValueError(f'A consulta {lang} não parece estar nesse idioma')
        key=(pair['pt'].strip().casefold(),pair['en'].strip().casefold())
        if key[0]==key[1] or key in seen:raise ValueError('Par duplicado ou sem tradução PT/EN')
        seen.add(key)


QUERIES='''Responda apenas JSON. Construa pares equivalentes de consultas para
pesquisar o recorte e suas lacunas no corpus técnico. Cada par contém pt em
português brasileiro e en em inglês técnico; mesma intenção, sem criar requisitos
ou fatos. Use sinônimos profissionais e siglas pertinentes, sem acumular todo o
escopo numa consulta. Consultas anteriores podem estar em qualquer idioma; sempre
gere os dois campos. Máximo limite pares de 3 a 40 palavras em cada campo.
JSON {"pares":[{"pt":"...","en":"..."}]}.
'''


def bilingual_search(index,pairs,limit,exclude=()):
    """Fusão RRF: nenhum idioma desaparece por corte da lista de consultas."""
    ranked={};traces=[]
    for pair in pairs:
        for lang in ('pt','en'):
            results=index.search(pair[lang],limit=limit,exclude=exclude)
            traces.append({**index.last_query_trace,'query_language':lang})
            for rank,row in enumerate(results,1):
                key=row.get('content_hash',row['chunk_id'])
                entry=ranked.setdefault(key,dict(row=row,score=0.,queries=[]))
                entry['score']+=1/(60+rank)
                entry['queries'].append(dict(language=lang,query=pair[lang],rank=rank))
    output=[]
    for entry in sorted(ranked.values(),key=lambda e:(-e['score'],e['row']['chunk_id'])):
        row={**entry['row'],'bilingual_retrieval':dict(rrf=entry['score'],queries=entry['queries'])}
        if not re.fullmatch(r'[a-z]{2}',str(row.get('language',''))) or row.get('language')=='und':
            signal=detect_language(row['texto']);row.update(language=signal['language'],language_detection=signal)
        output.append(row)
    return output,traces


LOCALE_AUDIT='''Responda apenas JSON. Revise os blocos em português brasileiro e
terminologia técnica usual no Brasil. Não imponha uma tradução literal a termos
profissionais consolidados. Verifique se empréstimos técnicos são compreensíveis,
sem frases inteiras em inglês ou português europeu não contextualizado. Preserve
nomes próprios, siglas, fórmulas e o significado técnico. Não reescreva nem invente
conhecimento. Avalie todos os IDs exatamente uma vez.
JSON {"avaliacoes":[{"id":"B...","pt_br":true,"terminologia_br":true,"motivo":"..."}]}.
'''


def audit_blocks(blocks,calls,batch_size=8):
    from .common import exact_rows, require, text
    reviews=[];corrections=[]
    for start in range(0,len(blocks),batch_size):
        batch=blocks[start:start+batch_size]
        def validate(data):
            exact_rows(data.get('avaliacoes'),[b['id'] for b in batch])
            for r in data['avaliacoes']:
                require(type(r.get('pt_br')) is bool and type(r.get('terminologia_br')) is bool
                        and text(r.get('motivo')),'Parecer linguístico incompleto')
        data=calls.call('locale',LOCALE_AUDIT+POLICY,dict(blocos=batch),validate)
        for r in data['avaliacoes']:
            block=next(b for b in batch if b['id']==r['id'])
            issues=lint_ptbr(block['subtitulo']+' '+block['texto'])
            reviews.append({**r,'alertas_locais':issues})
            if not r['pt_br'] or not r['terminologia_br'] or issues:
                corrections.append(dict(blocos=[r['id']],problema='PT-BR: '+r['motivo']+'; '+'; '.join(issues)))
    return dict(avaliacoes=reviews,correcoes=corrections)


def language_counts(rows):
    return dict(Counter(r.get('language','und') for r in rows))
