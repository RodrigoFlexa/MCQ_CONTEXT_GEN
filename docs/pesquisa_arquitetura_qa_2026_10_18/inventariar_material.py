"""Inventário dos trechos salvos nas seleções; não avalia sua veracidade.

Execução na raiz: python -X utf8 docs/pesquisa_arquitetura_qa_2026_10_18/inventariar_material.py
Sem rede, sem modelos, sem mudanças nos artefatos do pipeline.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ORIGENS = (
    'saida_producao_v3_correcao_azure',
    'saida_sistemas_de_lastro_v4_notas',
    'saida_mais_4_topicos_v4_nano_low',
    'saida_ultimos_5_topicos_v4_nano_low',
)


def main():
    occurrences, unique, files = Counter(), {}, []
    for origem in ORIGENS:
        for path in sorted((ROOT / 'pipeline/inventario' / origem).glob('subtopicos/*/selecao.json')):
            data = json.loads(path.read_text(encoding='utf-8'))
            relative = path.relative_to(ROOT).as_posix()
            files.append({'arquivo': relative, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            for aid, assunto in data.get('assuntos', {}).items():
                for trecho in assunto.get('trechos', []):
                    occurrences[trecho['collection']] += 1
                    entry = unique.setdefault(trecho['chunk_id'], {
                        'trecho': trecho, 'primeira_ocorrencia': relative, 'assunto': aid,
                        'ocorrencias': 0,
                    })
                    entry['ocorrencias'] += 1
    stats = defaultdict(Counter)
    for entry in unique.values():
        t = entry['trecho']
        s = stats[t['collection']]
        s['trechos_distintos_por_chunk_id'] += 1
        s['sem_pagina_inicial'] += t.get('page_ini') is None
        s['com_numero_mascarado'] += '<NUMBER>' in t['texto']
        s['fronteira_documental_desconhecida'] += 'unknown' in t.get('source_boundary', '')
    wanted = (
        ('entrevista_com_afirmacao_absoluta', lambda t: t['collection'] == 'regis' and 'Entrevistas' in t.get('title', '') and 'without causing' in t['texto']),
        ('principio_em_material_concatenado', lambda t: t['collection'] == 'petroles' and 'massas específicas da água' in t['texto']),
        ('numeros_essenciais_mascarados', lambda t: t['collection'] == 'petroles' and 'não pode conter mais do que <NUMBER>' in t['texto']),
        ('mecanismo_em_relatorio_incidente', lambda t: t['collection'] == 'anp' and 'bombas de deslocamento positivo' in t['texto']),
        ('descricao_instalacao_especifica', lambda t: t['collection'] == 'anp' and '3.1.1. Características da planta' in t['texto']),
        ('guia_com_contexto_estrangeiro', lambda t: t['collection'] == 'hse' and 'FPSOs/FSUs in the UKCS' in t['texto']),
        ('similaridade_lexical_fora_do_alvo', lambda t: t['collection'] == 'hse' and 'mineral insulating oil' in t['texto']),
        ('alerta_com_recomendacao_e_limite', lambda t: t['collection'] == 'bsee' and 'Latex gloves' in t['texto']),
    )
    cases = []
    for label, predicate in wanted:
        matches = [e for e in unique.values() if predicate(e['trecho'])]
        if not matches:
            raise ValueError(f'Caso não encontrado: {label}')
        e, = matches[:1]
        t = e['trecho']
        cases.append({
            'caso': label, 'arquivo': e['primeira_ocorrencia'], 'assunto': e['assunto'],
            **{k: t.get(k) for k in ('chunk_id', 'collection', 'document_id', 'title', 'page_ini', 'page_fim', 'linha_ini', 'linha_fim', 'jurisdiction', 'language')},
            'texto_sha256': hashlib.sha256(t['texto'].encode('utf-8')).hexdigest(),
            'nota': 'Exemplo intencional para leitura qualitativa; não é amostra aleatória nem rótulo de verdade.',
        })
    result = {
        'escopo': 'Seleções versionadas de quatro execuções; não é o corpus bruto completo nem apenas o piloto v5.',
        'metodo': 'Contagem de ocorrências; deduplicação por chunk_id. Janelas sobrepostas e cópias entre coleções podem permanecer.',
        'arquivos_selecao': len(files), 'ocorrencias': sum(occurrences.values()),
        'trechos_distintos_por_chunk_id': len(unique),
        'ocorrencias_por_colecao': dict(sorted(occurrences.items())),
        'indicadores_estruturais_por_colecao': {k: dict(v) for k, v in sorted(stats.items())},
        'casos_para_inspecao': cases, 'fontes_locais': files,
    }
    (OUT / 'inventario_material.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('arquivos_selecao', 'ocorrencias', 'trechos_distintos_por_chunk_id', 'indicadores_estruturais_por_colecao')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
