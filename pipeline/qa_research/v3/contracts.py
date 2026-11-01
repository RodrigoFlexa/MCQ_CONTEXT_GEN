"""Contratos pequenos, com localização de erro; conteúdo é julgado na revisão."""
import re

VERSION = 'v3-contracts-3-context'
TYPES = ('conceito','mecanismo','consequencia','diagnostico','decisao','procedimento')
CRITERIA = ('fundamentada','correta','autonoma','determinada','sem_pistas','classe','composicao','pt_br','distinta','escopo')


def require(ok, message):
    if not ok: raise ValueError(message)


def text(v): return isinstance(v,str) and bool(v.strip())


def rows(v, location):
    require(isinstance(v,list), location+': esperado array')
    require(all(isinstance(r,dict) and text(r.get('id')) and re.fullmatch(r'[A-Za-z0-9_-]{1,64}',r['id']) for r in v),location+': objetos com id seguro esperados')
    require(len({r['id'] for r in v})==len(v),location+': IDs repetidos')
    return v


def exact(v, expected, location):
    rows(v,location); require({r['id'] for r in v}==set(expected),location+': cubra exatamente os IDs enviados')


def strings(v, location):
    require(isinstance(v,list) and all(text(s) for s in v),location+': esperado array de strings não vazias')


def refs(v, allowed, location, empty=False):
    strings(v,location)
    require((bool(v) or empty) and len(set(v))==len(v) and set(v)<=set(allowed),location+': referências vazias, repetidas ou desconhecidas')


def pairs(v, location, empty=False, max_words=16):
    require(isinstance(v,list) and (bool(v) or empty),location+': esperado array de pares pt/en')
    for p in v:
        require(isinstance(p,dict) and text(p.get('pt')) and text(p.get('en')) and p['pt'].casefold()!=p['en'].casefold(),location+': cada par precisa de consultas distintas pt/en')
        require(all(len(p[lang].split())<=max_words for lang in ('pt','en')),location+': consultas curtas de até '+str(max_words)+' palavras por idioma')
    require(len(v)<=3,location+': no máximo três pares pt/en')


def plan(d, entrada):
    points=rows(d.get('pontos'),'pontos'); sections=rows(d.get('secoes'),'secoes')
    require(points and sections,'Plano precisa de pontos e seções')
    for p in points:
        require(text(p.get('ancora')) and p['ancora'] in entrada['frase_especialista'],p['id']+'.ancora: use citação literal da frase')
        require(text(p.get('descricao')) and type(p.get('prioritario')) is bool,p['id']+': descrição e prioritario booleano obrigatórios')
    known={p['id'] for p in points}; covered=set()
    for s in sections:
        require(text(s.get('titulo')),s['id']+'.titulo: ausente')
        refs(s.get('pontos'),known,s['id']+'.pontos'); covered.update(s['pontos'])
        pairs(s.get('consultas'),s['id']+'.consultas')
    require(covered==known,'secoes.pontos: todos os pontos precisam ser associados')


def section(d, sources):
    require(text(d.get('titulo')) and text(d.get('texto')),'seção: titulo e texto obrigatórios')
    refs(d.get('fontes'),sources,'seção.fontes')
    strings(d.get('complementos'),'seção.complementos')
    strings(d.get('lacunas'),'seção.lacunas')
    require(d['fontes'] or d['complementos'],'seção: declare fundamento ou complementos conceituais')


def review(d, sections, points):
    exact(d.get('secoes'),sections,'secoes'); exact(d.get('cobertura'),points,'cobertura')
    for r in d['secoes']:
        require(r.get('decisao') in ('liberar','corrigir') and text(r.get('motivo')),r['id']+': parecer inválido')
        require(isinstance(r.get('correcao'),str),r['id']+'.correcao: string esperada')
        require(r['decisao']!='corrigir' or text(r['correcao']),r['id']+': indique a correção necessária')
        pairs(r.get('consultas'),r['id']+'.consultas',empty=True)
        strings(r.get('limites'),'seção.limites')
        gaps=r.get('lacunas_essenciais')
        require(isinstance(gaps,list),r['id']+'.lacunas_essenciais: esperado array')
        require(all(isinstance(g,dict) and g.get('ponto') in points and text(g.get('descricao')) for g in gaps),
            r['id']+'.lacunas_essenciais: ponto conhecido e descrição obrigatórios')
        require(len({g['ponto'] for g in gaps})==len(gaps),r['id']+': lacunas essenciais repetidas')
    for p in d['cobertura']:
        require(p.get('estado') in ('atendido','parcial','ausente') and text(p.get('motivo')),p['id']+': cobertura inválida')
        refs(p.get('secoes'),sections,p['id']+'.secoes',empty=p['estado']=='ausente')
    strings(d.get('omissoes_escopo'),'omissoes_escopo')
    coverage={p['id']:p for p in d['cobertura']}
    for r in d['secoes']:
        for gap in r['lacunas_essenciais']:
            require(coverage[gap['ponto']]['estado']!='atendido',gap['ponto']+': lacuna essencial contradiz cobertura atendida')


def candidate(q, sections, points):
    require(q.get('tipo') in TYPES and q.get('composicao') in ('simples','composta') and type(q.get('cenario')) is bool,q['id']+': classe/composição/cenario inválidos')
    require(all(text(q.get(k)) for k in ('pergunta','resposta','conhecimento')),q['id']+': pergunta, resposta e conhecimento obrigatórios')
    require(isinstance(q.get('ponte'),str) and (q['composicao']=='simples' or text(q['ponte'])),q['id']+'.ponte: explique a combinação necessária')
    refs(q.get('pontos'),points,q['id']+'.pontos')
    require(isinstance(q.get('fundamentos'),list) and q['fundamentos'],q['id']+'.fundamentos: cite o contexto')
    for e in q['fundamentos']:
        require(isinstance(e,dict) and e.get('secao') in sections and text(e.get('trecho')) and e['trecho'] in sections[e['secao']]['texto'],q['id']+'.fundamentos: passagem literal e seção existente obrigatórias')


def authored(d, sections, points, limit):
    qs=rows(d.get('questoes'),'questoes'); require(len(qs)<=limit,'questoes: excedeu o limite do lote')
    for q in qs: candidate(q,sections,points)
    strings(d.get('impedimentos'),'impedimentos')


def solutions(d, questions):
    exact(d.get('resolucoes'),questions,'resolucoes')
    for r in d['resolucoes']:
        require(text(r.get('resposta')),r['id']+'.resposta: vazia'); strings(r.get('ambiguidades'),r['id']+'.ambiguidades')


def judged(d, questions, admitted):
    exact(d.get('avaliacoes'),questions,'avaliacoes'); known=set(questions)|set(admitted)
    decisions={r['id']:r for r in d['avaliacoes']}
    for r in d['avaliacoes']:
        require(r.get('decisao') in ('admitir','corrigir','descartar','lacuna_documental') and text(r.get('motivo')),r['id']+': decisão inválida')
        require(isinstance(r.get('criterios'),dict) and all(type(r['criterios'].get(k)) is bool for k in CRITERIA),r['id']+': critérios booleanos obrigatórios')
        dup=r.get('duplicada_de')
        require(dup is None or (dup in known and dup!=r['id']),r['id']+': duplicata desconhecida')
        require(r['decisao']!='admitir' or (all(r['criterios'][k] for k in CRITERIA) and dup is None),r['id']+': admissão contradiz critérios')
        if dup:
            require(r['decisao']=='descartar' and (dup in admitted or decisions[dup]['decisao']=='admitir'),r['id']+': duplicata precisa apontar para uma admitida')


def refined(d, originals, sections, points):
    exact(d.get('itens'),originals,'itens')
    for r in d['itens']:
        require(r.get('decisao') in ('corrigida','descartar','lacuna_documental') and isinstance(r.get('motivo'),str),r['id']+': refino inválido')
        if r['decisao']=='corrigida':
            q=r.get('questao'); require(isinstance(q,dict) and q.get('id')==r['id'],r['id']+': devolva a questão completa')
            candidate(q,sections,points)
            require(all(q[k]==originals[r['id']][k] for k in ('tipo','composicao','conhecimento','pontos')),r['id']+': preserve conhecimento, pontos, classe e composição')
