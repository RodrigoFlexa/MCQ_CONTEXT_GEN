"""Compara experimentos e cria uma revisão humana cega conjunta; não chama modelos."""
import argparse
import csv
import json
import math
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json, read_jsonl, sha, write_jsonl

HUMAN_FIELDS = ('correta', 'sustentada', 'autonoma', 'competencia', 'sem_pista', 'escopo', 'nao_redundante')


def binary(value):
    v = str(value).strip().casefold()
    if v in ('sim', 's', 'yes', 'true', '1'):
        return True
    if v in ('nao', 'não', 'n', 'no', 'false', '0'):
        return False
    return None


def interval(successes, total):
    if not total:
        return None
    z, p = 1.96, successes / total
    center = (p + z*z/(2*total)) / (1 + z*z/total)
    delta = z * math.sqrt(p*(1-p)/total + z*z/(4*total*total)) / (1 + z*z/total)
    return [round(max(0, center-delta), 4), round(min(1, center+delta), 4)]


def read_review(path):
    if not path.exists():
        return {}
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return {r['id_cego']: r for r in csv.DictReader(stream)}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--experimentos', nargs='+', required=True)
    p.add_argument('--saida', required=True)
    a = p.parse_args(argv)
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    combined_path = out / 'revisao_cega.csv'
    annotated = read_review(combined_path)
    summaries, combined, mapping, objectives, blind_sources = [], [], [], [], []
    for directory in a.experimentos:
        root = Path(directory)
        summary = read_json(root / 'resumo.json')
        if not summary:
            summaries.append({'experimento': str(root), 'erro': 'sem resumo; execução não concluída ou não iniciada'})
            continue
        rows = {r['id']: r for r in read_jsonl(root / 'questoes_todas.jsonl')}
        objectives.append(set(r['objetivo_id'] for r in rows.values() if r.get('objetivo_id')))
        aliases = read_jsonl(root / 'mapa_revisao.jsonl')
        human = {**read_review(root / 'revisao_humana.csv'), **annotated}
        tp = fp = fn = tn = labeled = undecided = 0
        for item in aliases:
            q = rows[item['id']]
            label = human.get(item['id_cego'], {})
            values = [binary(label.get(k, '')) for k in HUMAN_FIELDS]
            if all(v is not None for v in values):
                valid, accepted = all(values), q['status'] == 'aprovada'
                labeled += 1
                if q['status'] in ('pendente_validacao', 'falha_execucao'):
                    undecided += 1
                else:
                    tp += int(valid and accepted)
                    fp += int(not valid and accepted)
                    fn += int(valid and not accepted)
                    tn += int(not valid and not accepted)
            combined.append({'id_cego': item['id_cego'], 'pergunta': q['pergunta'], 'resposta': q['resposta'],
                             'explicacao': q['explicacao'], 'rubrica': '; '.join(q['rubrica']),
                             **{k: label.get(k, '') for k in (*HUMAN_FIELDS, 'comentario')}})
            mapping.append({**item, 'experimento': str(root)})
            blind_sources.append({'id_cego': item['id_cego'], 'evidencias': q.get('evidencias', [])})
        accepted = summary['total_aprovadas_automaticamente']
        usage = summary.get('uso', {})
        tokens = usage.get('prompt_tokens', 0) + usage.get('completion_tokens', 0)
        summaries.append({'experimento': str(root), 'configuracao': summary['configuracao'],
                          'modo': summary['modo'], 'aprovadas_automaticamente': accepted,
                          'metas_atingidas': summary['metas_atingidas'], 'subtopicos': summary['subtopicos'],
                          'tentativas_api': usage.get('tentativas_api'), 'tokens': tokens,
                          'tokens_por_aprovada_automatica': round(tokens / accepted) if accepted else None,
                          'avaliadas_por_humano': labeled,
                          'revisadas_sem_decisao_automatica': undecided,
                          'aprovacoes_corretas': tp, 'falsas_aprovacoes': fp,
                          'falsas_reprovacoes': fn, 'reprovacoes_corretas': tn,
                          'precisao_nas_aprovadas_revisadas': tp/(tp+fp) if tp+fp else None,
                          'precisao_intervalo_wilson_95': interval(tp, tp+fp),
                          'limite': 'rótulos humanos incompletos não entram nas métricas; sem rótulos não há precisão medida'})
    # Mantém avaliações existentes quando novas execuções entram na bateria.
    fields = ['id_cego', 'pergunta', 'resposta', 'explicacao', 'rubrica', *HUMAN_FIELDS, 'comentario']
    with combined_path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(combined, key=lambda r: sha(r['id_cego'], 40)))
    atomic_json(out / 'mapa_revisao.json', mapping)
    write_jsonl(out / 'evidencias_revisao_cega.jsonl', blind_sources)
    result = {'experimentos': summaries,
              'objetivos_em_comum': sorted(set.intersection(*objectives)) if objectives else [],
              'interpretacao': 'Modo cota pode consumir objetivos diferentes. Compare também os objetivos comuns; '
                               'direta versus nota controla a exibição da nota; complemento muda as evidências. '
                               'O cache compartilhado torna o consumo observado dependente da ordem; '
                               'não representa custo de execução sem cache. '
                               'Aprovação automática não mede qualidade humana nem prova ausência de erro.'}
    atomic_json(out / 'comparacao.json', result)
    lines = ['# Comparação QA v11', '', result['interpretacao'], '',
             '| Configuração | Aprovadas automaticamente | Tentativas API | Tokens | Revisadas por humano |',
             '|---|---:|---:|---:|---:|']
    for r in summaries:
        lines.append(f"| {r.get('configuracao', r['experimento'])} | {r.get('aprovadas_automaticamente', '—')} | "
                     f"{r.get('tentativas_api', '—')} | {r.get('tokens', '—')} | {r.get('avaliadas_por_humano', '—')} |")
    lines += ['', f"Objetivos presentes em todos os experimentos disponíveis: {len(result['objetivos_em_comum'])}.", '',
              'Preencha revisao_cega.csv (sim/não) e repita este comando para calcular precisão e erros do juiz.']
    (out / 'comparacao.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'saida': str(out), 'experimentos': len(summaries)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
