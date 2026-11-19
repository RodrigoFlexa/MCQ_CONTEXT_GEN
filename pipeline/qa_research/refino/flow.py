"""Refino de um documento: roteiro → rascunhos → pesquisa → consolidação → redação → revisão.

Agentes (todos com o deployment configurado em `models`):
- planejador: roteiro novo a partir do feedback do especialista e da base revisada;
- redatores: K perspectivas escrevem cada seção sem consulta, em afirmações atômicas;
- pesquisadores: buscam nos corpora por objetivo de conhecimento, com reflexão sobre o
  que falta (até `research_rounds` rodadas), e verificam as afirmações dos redatores;
- consolidador da seção: funde afirmações, achados e blocos revisados em unidades únicas;
- redator da seção: escreve os blocos usando cada unidade exatamente uma vez;
- consolidador do documento: elimina redundância entre seções e entre documentos;
- revisor: cobertura das lacunas e problemas por bloco; um reparo dirigido;
- editor de estilo: percorre os capítulos em ordem, expande cada sigla na primeira ocorrência,
  tira o texto que fala do próprio documento e os travessões, sem mudar o conteúdo.
Chamadas repetidas com a mesma entrada são reaproveitadas do cache (retomada).
"""
import asyncio
import json
import re
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.v3.runtime import CallFailure, Fatal, stamp
from . import VERSION, contracts as C, prompts as P, semantica as S, textos as T
from .retrieval import public


def base_blocks(entrada):
    return [dict(id=b['id'], capitulo=c['titulo'], subtitulo=b['subtitulo'], texto=b['texto'],
                 anotacoes=b.get('anotacoes', []))
            for c in entrada['base']['capitulos'] for b in c['blocos']]


def gap_rows(entrada):
    fb = entrada['feedback']
    rows = [dict(id=g['id'], descricao=g['descricao'], origem='comentario_especialista') for g in fb['lacunas']]
    rows += [dict(id=g['id'], descricao=f"{g['topico']} ({g['situacao']}): {g['aspectos']}",
                  origem='analise_llm_curada_pelo_especialista') for g in fb['lacunas_llm']]
    return rows


def meta(entrada):
    return {k: entrada[k] for k in ('id', 'titulo', 'topico', 'subtopico', 'frase_especialista')}


def concepts_for(mapa, item):
    if not mapa:
        return dict(proprios=[], de_outros=[])
    own = [dict(conceito=c['conceito'], motivo=c.get('motivo', ''), outros_documentos=[m['doc'] for m in c.get('mencoes', [])])
           for c in mapa['conceitos'] if c['dono'] == item]
    others = [dict(conceito=c['conceito'], dono=c['dono'], enfoque=m['enfoque'])
              for c in mapa['conceitos'] for m in c.get('mencoes', []) if m['doc'] == item]
    return dict(proprios=own, de_outros=others)


async def concept_map(entradas, calls, config):
    docs = [dict(id=e['id'], titulo=e['titulo'], frase_especialista=e['frase_especialista'],
                 capitulos=[c['titulo'] for c in e['base']['capitulos']],
                 subtitulos=[b['subtitulo'][:70] for c in e['base']['capitulos'] for b in c['blocos']][:20],
                 lacunas=[g['descricao'][:100] for g in gap_rows(e)][:10]) for e in entradas]
    ids = [d['id'] for d in docs]
    return await calls.call('plan', 'mapa_conceitos', dict(documentos=docs), lambda d: C.mapa(d, ids), system=P.MAPA)


class Refino:
    def __init__(self, entrada, acervo, calls, config, folder, mapa=None, outros_textos=None, progress=print):
        self.e, self.acervo, self.calls, self.cfg = entrada, acervo, calls, config
        self.folder, self.progress = Path(folder), progress
        self.conceitos = concepts_for(mapa, entrada['id'])
        self.base = base_blocks(entrada)
        self.gaps = gap_rows(entrada)
        self.outros = outros_textos or {}
        self.summary = dict(schema=VERSION, item=entrada['id'], titulo=entrada['titulo'], status='em_andamento',
                            inicio=stamp(), etapas={}, falhas=[], avisos=[])

    # ---------------------------------------------------------------- utilidades
    def save(self, name, data):
        atomic_json(self.folder / name, data)

    def stage(self, name, **info):
        self.summary['etapas'][name] = dict(fim=stamp(), **info)
        self.save('resumo.json', self.summary)
        self.progress(f'[{self.e["id"]}] etapa concluída: {name}', flush=True)

    def fail(self, where, exc):
        self.summary['falhas'].append(dict(etapa=where, erro=type(exc).__name__ + ': ' + str(exc)[:600]))
        self.save('resumo.json', self.summary)
        self.progress(f'[{self.e["id"]}] falha em {where}: {type(exc).__name__}', flush=True)

    async def call(self, role, tag, payload, validate, system, tokens=None):
        return await self.calls.call(role, tag, payload, validate, system=system, tokens=tokens)

    # ---------------------------------------------------------------- roteiro
    async def plan(self):
        fb = self.e['feedback']
        payload = dict(documento=meta(self.e),
            feedback=dict(comentario=fb['comentario'], comentarios_no_corpo=fb['comentarios_no_corpo'],
                          analise_llm=fb['analise_llm'], problemas=fb['problemas'], encaminhamento=fb['nivel_nome'],
                          evidencia_inadequacao=fb['evidencia_inadequacao']),
            lacunas=self.gaps, base=self.base,
            removidos_pelo_especialista=[dict(tipo=r['tipo'], secao=r['secao']) for r in self.e.get('removidos', [])],
            conceitos=self.conceitos,
            limites=dict(min_secoes=self.cfg['min_sections'], max_secoes=self.cfg['max_sections']))
        gap_ids, block_ids = [g['id'] for g in self.gaps], [b['id'] for b in self.base]
        check = lambda d: C.plano(d, gap_ids, block_ids, self.cfg['min_sections'], self.cfg['max_sections'],
                                  default_title=self.e['titulo'])
        # O roteiro é a etapa da qual tudo depende: mais espaço de saída (o raciocínio também conta)
        # e uma segunda rodada de tentativas antes de desistir do documento.
        tokens = self.cfg.get('plan_tokens', 32000)
        try:
            plan = await self.call('plan', 'roteiro', payload, check, P.PLANO, tokens=tokens)
        except (Fatal, BudgetExceeded):
            raise
        except Exception as exc:
            self.summary['avisos'].append('roteiro: primeira rodada falhou (' + str(exc)[:300] + '); repetindo')
            plan = await self.call('plan', 'roteiro_2', payload, check, P.PLANO, tokens=tokens)
        self.save('roteiro.json', plan)
        self.stage('roteiro', secoes=len(plan['secoes']), blocos_descartados=len(plan.get('blocos_descartados', [])),
                   lacunas_fora_de_escopo=len(plan.get('lacunas_fora_de_escopo', [])))
        return plan

    # ---------------------------------------------------------------- seção
    def outline(self, plan):
        return [dict(id=s['id'], titulo=s['titulo'], objetivo=s['objetivo']) for s in plan['secoes']]

    def section_view(self, s):
        return dict(id=s['id'], tipo=s['tipo'], titulo=s['titulo'], objetivo=s['objetivo'],
                    conhecimentos=s['conhecimentos'],
                    lacunas=[g for g in self.gaps if any(g['id'] in k.get('lacunas', []) for k in s['conhecimentos'])])

    async def drafts(self, plan, s):
        k_ids = [k['id'] for k in s['conhecimentos']]
        payload = dict(documento=meta(self.e), roteiro=self.outline(plan), secao=self.section_view(s),
                       conceitos=self.conceitos)

        async def one(index, writer):
            system = P.RASCUNHO + '\nPerspectiva deste redator: ' + P.PERSPECTIVAS[writer['perspectiva']]
            data = await self.call('draft', f"{s['id']}_rascunho_{writer['id']}", dict(payload, redator=writer['id']),
                                   lambda d: C.rascunho(d, k_ids, self.cfg['min_claims'], self.cfg['max_claims']), system)
            return [dict(a, id=f"W{index}{a['id']}", redator=writer['id']) for a in data['afirmacoes']]

        results = await asyncio.gather(*(one(i, w) for i, w in enumerate(self.cfg['writers'], 1)), return_exceptions=True)
        claims = []
        for writer, result in zip(self.cfg['writers'], results):
            if isinstance(result, (Fatal, BudgetExceeded)):
                raise result
            if isinstance(result, BaseException):
                self.fail(f"{s['id']}_rascunho_{writer['id']}", result)
                continue
            claims += result
        return claims

    async def research(self, s, claims):
        k_ids = [k['id'] for k in s['conhecimentos']]
        claim_ids = [c['id'] for c in claims]
        seen, passages, findings, verifs, rounds = set(), {}, [], {}, []
        queries, asked = list(s['consultas']), list(s['consultas'])
        missing = list(k_ids)
        for r in range(1, self.cfg['research_rounds'] + 1):
            chosen, trace = await asyncio.to_thread(self.acervo.query, queries, self.cfg['retrieval_candidates'], seen,
                                                    self.cfg['max_per_document'], self.cfg['read_candidates'])
            seen |= {p['id'] for p in chosen}
            if not chosen:
                rounds.append(dict(rodada=r, consultas=queries, motivo='nenhuma passagem nova', busca=trace))
                break
            packed, size = [], 0
            for p in chosen:
                row = {k: p.get(k) for k in ('id', 'texto', 'collection', 'title', 'language', 'jurisdiction', 'document_type')}
                size += len(json.dumps(row, ensure_ascii=False))
                if size > self.cfg['max_passage_chars']:
                    break
                packed.append(row)
                passages[p['id']] = p
            payload = dict(secao=self.section_view(s), passagens=packed,
                           afirmacoes=[dict(id=c['id'], texto=c['texto']) for c in claims],
                           achados_anteriores=[dict(id=f['id'], texto=f['texto']) for f in findings],
                           consultas_anteriores=asked, conhecimentos_sem_suporte=missing)
            pids = [p['id'] for p in packed]
            try:
                data = await self.call('read', f"{s['id']}_leitura_{r}", payload,
                                       lambda d: C.leitura(d, pids, k_ids, claim_ids), P.LEITURA)
            except (Fatal, BudgetExceeded):
                raise
            except Exception as exc:
                # A pesquisa para aqui; a seção segue com o que já foi achado e com o conhecimento dos
                # redatores (estatuto "modelo"/"consenso_modelos"), em vez de ficar vazia.
                self.summary['avisos'].append(f"{s['id']}: leitura {r} falhou ({type(exc).__name__}); "
                                              'seção completada com o achado até aqui e o conhecimento dos redatores')
                rounds.append(dict(rodada=r, consultas=queries, busca=trace, falha=type(exc).__name__ + ': ' + str(exc)[:300]))
                break
            for n, f in enumerate(data['achados'], 1):
                findings.append(dict(f, id=f"R{r}F{n:02d}", id_modelo=f['id']))
            for v in data.get('verificacoes', []):
                verifs.setdefault(v['afirmacao'], []).append(dict(estado=v['estado'], fontes=v['fontes'],
                                                                  nota=v.get('nota', ''), rodada=r))
            missing = data.get('lacunas', [])
            rounds.append(dict(rodada=r, consultas=queries, busca=trace, passagens=pids,
                               achados=len(data['achados']), lacunas=missing))
            new = [q for q in data.get('novas_consultas', []) if q not in asked]
            if not missing or not new:
                break
            queries = new
            asked += new
        return dict(passagens=passages, achados=findings, verificacoes=verifs, rodadas=rounds, lacunas_finais=missing)

    def claim_status(self, claim, verifs):
        states = {v['estado'] for v in verifs.get(claim['id'], [])}
        return 'apoia' if 'apoia' in states else 'contradiz' if 'contradiz' in states else 'sem_evidencia'

    async def consolidate(self, s, claims, found):
        k_ids = [k['id'] for k in s['conhecimentos']]
        verifs = found['verificacoes']
        contradicted = {c['id'] for c in claims if self.claim_status(c, verifs) == 'contradiz'}
        specific = {c['id'] for c in claims if c['especifico']}
        by_id = {b['id']: b for b in self.base}
        blocks = [by_id[b] for b in s['blocos_base']]
        payload = dict(documento=meta(self.e), secao=self.section_view(s),
            afirmacoes=[dict(id=c['id'], texto=c['texto'], tipo=c['tipo'], redator=c['redator'], especifico=c['especifico'],
                             verificacao=self.claim_status(c, verifs),
                             nota=' | '.join(v['nota'] for v in verifs.get(c['id'], []) if v.get('nota'))) for c in claims],
            achados=[dict(id=f['id'], texto=f['texto'], condicoes=f.get('condicoes', ''), jurisdicao=f.get('jurisdicao', ''))
                     for f in found['achados']],
            blocos=[dict(id=b['id'], subtitulo=b['subtitulo'], texto=b['texto'], anotacoes=b['anotacoes']) for b in blocks],
            conceitos=self.conceitos, politica=dict(valores_sem_fonte=self.cfg['allow_values_without_source']))
        data = await self.call('consolidate', f"{s['id']}_consolidacao", payload,
            lambda d: C.consolidacao(d, [c['id'] for c in claims], [f['id'] for f in found['achados']],
                                     s['blocos_base'], k_ids, contradicted, specific,
                                     self.cfg['allow_values_without_source']), P.CONSOLIDACAO)
        expected = {c['id'] for c in claims} | {f['id'] for f in found['achados']} | set(s['blocos_base'])
        used = {x for u in data['unidades'] for v in u['origem'].values() for x in v} | {d['ref'] for d in data.get('descartadas', [])}
        data = dict(data, nao_contabilizadas=sorted(expected - used))
        claims_by_id = {c['id']: c for c in claims}
        findings_by_id = {f['id']: f for f in found['achados']}
        units = []
        for u in data['unidades']:
            origin = u['origem']
            sources = set()
            for f in origin.get('achados', []):
                sources |= set(findings_by_id[f]['fontes'])
            for a in origin.get('afirmacoes', []):
                for v in verifs.get(a, []):
                    if v['estado'] == 'apoia':
                        sources |= set(v['fontes'])
            writers = {claims_by_id[a]['redator'] for a in origin.get('afirmacoes', [])}
            status = ('evidencia' if sources else 'base_revisada' if origin.get('blocos')
                      else 'consenso_modelos' if len(writers) >= 2 else 'modelo')
            units.append(dict(u, id=s['id'] + u['id'], id_modelo=u['id'], estatuto=status,
                              redatores=sorted(writers), fontes=sorted(sources)))
        return units, data

    async def write(self, plan, s, units, neighbours=None):
        ids = [u['id_modelo'] for u in units]
        titles = self.outline(plan)
        position = next(i for i, t in enumerate(titles) if t['id'] == s['id'])
        payload = dict(documento=meta(self.e), secao=dict(id=s['id'], tipo=s['tipo'], titulo=s['titulo'], objetivo=s['objetivo']),
                       unidades=[dict(id=u['id_modelo'], texto=u['texto']) for u in units],
                       anterior=titles[position - 1] if position else None,
                       seguinte=titles[position + 1] if position + 1 < len(titles) else None,
                       roteiro=titles, conceitos=self.conceitos)
        if neighbours:
            payload['secoes_do_documento'] = neighbours
        data = await self.call('write', f"{s['id']}_redacao", payload, lambda d: C.redacao(d, ids, s['id']), P.REDACAO)
        mapping = {u['id_modelo']: u['id'] for u in units}
        return [dict(b, unidades=[mapping[x] for x in b['unidades']]) for b in data['blocos']]

    async def section(self, plan, s, neighbours=None):
        claims = await self.drafts(plan, s)
        if not claims:
            raise CallFailure(s['id'] + ': nenhum rascunho disponível')
        found = await self.research(s, claims)
        units, raw = await self.consolidate(s, claims, found)
        blocks = await self.write(plan, s, units, neighbours)
        return dict(secao=s, afirmacoes=claims, pesquisa=found, unidades=units, consolidacao=raw, blocos=blocks)

    # ---------------------------------------------------------------- documento
    def assemble(self, plan, done):
        chapters = []
        for s in plan['secoes']:
            if s['id'] in done:
                chapters.append(dict(titulo=s['titulo'], grupo=self.e['subtopico'], secao=s['id'],
                                     blocos=[dict(id=b['id'], subtitulo=b['subtitulo'], texto=b['texto'],
                                                  unidades=b['unidades']) for b in done[s['id']]['blocos']]))
        return dict(titulo=self.e['titulo'], capitulos=chapters)

    def block_list(self, document):
        return [dict(id=b['id'], secao=c['titulo'], subtitulo=b['subtitulo'], texto=b['texto'])
                for c in document['capitulos'] for b in c['blocos']]

    def cross_pairs(self, document, threshold):
        if not self.outros:
            return []
        mine = [(b['id'], s) for b in self.block_list(document) for s in T.sentences(b['texto'])]
        theirs = [(doc, s) for doc, sents in self.outros.items() for s in sents]
        if not mine or not theirs:
            return []
        vec = T.Vectors([s for _, s in mine] + [s for _, s in theirs]).vectors
        a, b = vec[:len(mine)], vec[len(mine):]
        pairs = []
        for i, va in enumerate(a):
            best = max(((T.Vectors.cosine(va, vb), j) for j, vb in enumerate(b)), default=(0, -1))
            if best[0] >= threshold:
                pairs.append(dict(bloco=mine[i][0], sentenca=mine[i][1], outro_documento=theirs[best[1]][0],
                                  sentenca_outro=theirs[best[1]][1], similaridade=round(best[0], 3)))
        return sorted(pairs, key=lambda p: -p['similaridade'])[:30]

    async def consolidate_document(self, document):
        history = []
        for r in range(1, self.cfg['consolidation_rounds'] + 1):
            red = T.redundancy(document, self.cfg['redundancy_threshold'])
            cross = self.cross_pairs(document, self.cfg['redundancy_threshold'])
            if not red['pares'] and not cross:
                history.append(dict(rodada=r, motivo='sem pares redundantes', taxa=red['taxa_redundancia']))
                break
            blocks = self.block_list(document)
            ids = [b['id'] for b in blocks]
            payload = dict(documento=meta(self.e), blocos=blocks, pares_internos=red['pares'][:40],
                           pares_com_outros_documentos=cross, conceitos=self.conceitos)
            data = await self.call('edit', f'consolidacao_documento_{r}', payload, lambda d: C.consolida_doc(d, ids), P.CONSOLIDA_DOC)
            applied = []
            for op in data['operacoes']:
                for c in document['capitulos']:
                    for b in c['blocos']:
                        if b['id'] == op['bloco']:
                            applied.append(dict(op, texto_anterior=b['texto']))
                            b['texto'] = op['novo_texto']
            after = T.redundancy(document, self.cfg['redundancy_threshold'])
            history.append(dict(rodada=r, pares_internos=red['n_pares'], pares_entre_documentos=len(cross),
                                taxa_antes=red['taxa_redundancia'], taxa_depois=after['taxa_redundancia'],
                                operacoes=applied))
            if not data['operacoes']:
                break
        return history

    async def coverage(self, blocks, tag):
        gap_ids = [g['id'] for g in self.gaps]
        if not gap_ids:
            return dict(cobertura=[])
        ids = [b['id'] for b in blocks]
        payload = dict(documento=meta(self.e), lacunas=self.gaps, blocos=blocks)
        return await self.call('review', tag, payload, lambda d: C.cobertura(d, gap_ids, ids), P.COBERTURA_BASE)

    def alerts(self, document, units):
        by_unit = {u['id']: u for u in units}
        out = []
        for c in document['capitulos']:
            for b in c['blocos']:
                out += [dict(bloco=b['id'], **i) for i in T.lint(b['subtitulo'] + ' ' + b['texto'])]
                statuses = {by_unit[u]['estatuto'] for u in b.get('unidades', []) if u in by_unit}
                if T.has_value(b['texto']) and not statuses & {'evidencia', 'base_revisada'}:
                    out.append(dict(bloco=b['id'], tipo='valor_sem_fonte', trecho=T.VALOR.search(b['texto'])[0]))
        return out

    async def review_and_repair(self, document, done, units):
        blocks = self.block_list(document)
        ids, gap_ids = [b['id'] for b in blocks], [g['id'] for g in self.gaps]
        payload = dict(documento=meta(self.e), lacunas=self.gaps, blocos=blocks,
                       alertas_locais=self.alerts(document, units), conceitos=self.conceitos)
        review = await self.call('review', 'revisao', payload, lambda d: C.revisao(d, gap_ids, ids), P.REVISAO)
        weak = {c['id'] for c in review['cobertura'] if c['estado'] != 'atendido'}
        problems = {}
        for p in review['problemas']:
            problems.setdefault(p['bloco'], []).append(p)
        repairs = []
        for c in document['capitulos']:
            targets = [b for b in c['blocos'] if b['id'] in problems]
            if not targets:
                continue
            sec = done[c['secao']]
            target_ids = [b['id'] for b in targets]
            related = [g for g in self.gaps if g['id'] in weak and any(g['id'] in k.get('lacunas', []) for k in sec['secao']['conhecimentos'])]
            payload = dict(documento=meta(self.e), blocos=[dict(id=b['id'], subtitulo=b['subtitulo'], texto=b['texto']) for b in targets],
                           problemas=[p for b in target_ids for p in problems[b]], lacunas_relacionadas=related,
                           unidades=[dict(id=u['id'], texto=u['texto'], estatuto=u['estatuto']) for u in sec['unidades']],
                           achados=[dict(id=f['id'], texto=f['texto']) for f in sec['pesquisa']['achados']],
                           conceitos=self.conceitos)
            try:
                data = await self.call('write', f"{c['secao']}_reparo", payload, lambda d: C.reparo(d, target_ids), P.REPARO)
            except (Fatal, BudgetExceeded):
                raise
            except Exception as exc:
                self.fail(c['secao'] + '_reparo', exc)
                continue
            fixed = {b['id']: b for b in data['blocos']}
            for b in targets:
                repairs.append(dict(bloco=b['id'], antes=b['texto'], depois=fixed[b['id']]['texto'], problemas=problems[b['id']]))
                b['subtitulo'], b['texto'] = fixed[b['id']]['subtitulo'], fixed[b['id']]['texto']
        return review, repairs

    async def polish(self, document):
        """Editor final, capítulo a capítulo: siglas na 1ª ocorrência do documento, sem metatexto nem enchimento.

        Falha num capítulo vira aviso (o capítulo fica como estava): é ajuste de forma."""
        before = T.style_report(document)
        changes, removed, glossary, filler = [], [], {}, []
        for c in document['capitulos']:
            pending, _ = T.acronyms(dict(capitulos=[c]), known=set(glossary))
            alerts = [dict(bloco=b['id'], **i) for b in c['blocos']
                      for i in T.style_issues(b['subtitulo'] + ' ' + b['texto']) + T.dependent_opening(b['texto'])]
            alerts += [dict(bloco=b, tipo='sigla_sem_expansao', trecho=s) for b, v in pending.items() for s in v]
            originals = [dict(id=b['id'], subtitulo=b['subtitulo'], texto=b['texto']) for b in c['blocos']]
            payload = dict(documento=meta(self.e), capitulo=c['titulo'], blocos=originals,
                           siglas_conhecidas={k: glossary[k] for k in sorted(glossary)}, alertas=alerts)
            try:
                data = await self.call('edit', f"{c['secao']}_polimento", payload,
                                       lambda d: C.polimento(d, originals, set(glossary)), P.POLIMENTO)
            except (Fatal, BudgetExceeded):
                raise
            except Exception as exc:
                self.summary['avisos'].append(f"polimento de {c['secao']} não aplicado: {type(exc).__name__}: {str(exc)[:300]}")
                continue
            known_before = set(glossary)
            for s in data.get('siglas_expandidas', []):
                glossary.setdefault(s['sigla'], s['expansao'])
            filler += data.get('enchimento_removido', [])
            fixed = {b['id']: b for b in data['blocos']}
            keep = []
            for b in c['blocos']:
                new = fixed[b['id']]
                if new.get('remover') is True:
                    removed.append(dict(bloco=b['id'], subtitulo=b['subtitulo'], texto=b['texto']))
                    continue
                if (new['subtitulo'], new['texto']) != (b['subtitulo'], b['texto']):
                    changes.append(dict(bloco=b['id'], antes=b['texto'], depois=new['texto']))
                b['subtitulo'], b['texto'] = new['subtitulo'], T.TRAVESSAO.sub(', ', new['texto'])
                keep.append(b)
            c['blocos'] = keep
            # Siglas ainda sem expansão na primeira ocorrência: o código insere a expansão informada.
            pending, _ = T.acronyms(dict(capitulos=[c]), known=known_before)
            expansions = {s['sigla']: s['expansao'] for s in data.get('siglas_expandidas', [])
                          if s['sigla'] not in known_before}
            for bid, items in pending.items():
                for sigla in items:
                    if sigla in expansions:
                        b = next(x for x in c['blocos'] if x['id'] == bid)
                        b['texto'] = re.sub(r'\b' + re.escape(sigla) + r'\b', f'{expansions[sigla]} ({sigla})', b['texto'], count=1)
        document['capitulos'] = [c for c in document['capitulos'] if c['blocos']]
        self.glossary = glossary
        return dict(antes=before, depois=T.style_report(document), blocos_alterados=len(changes),
                    blocos_removidos=removed, enchimento_removido=filler, glossario=glossary, alteracoes=changes)

    # ---------------------------------------------------------------- execução
    async def run(self):
        self.save('entrada.json', dict(id=self.e['id'], origem=self.e['origem'], lacunas=self.gaps,
                                       removidos=self.e.get('removidos', []), conceitos=self.conceitos))
        base_doc = dict(titulo=self.e['titulo'], capitulos=[dict(titulo=c['titulo'], grupo=c.get('grupo'), blocos=[
            dict(id=b['id'], subtitulo=b['subtitulo'], texto=b['texto']) for b in c['blocos']]) for c in self.e['base']['capitulos']])
        self.save('documento_base.json', T.clean(base_doc))
        (self.folder / 'documento_base.md').write_text(T.markdown(T.clean(base_doc)), encoding='utf-8')
        base_cov = None
        if self.cfg['evaluate_base']:
            try:
                base_cov = await self.coverage([dict(id=b['id'], subtitulo=b['subtitulo'], texto=b['texto']) for b in self.base],
                                               'cobertura_base')
                self.save('cobertura_base.json', base_cov)
            except (Fatal, BudgetExceeded):
                raise
            except Exception as exc:
                self.fail('cobertura_base', exc)
        plan = await self.plan()
        done = {}
        development = [s for s in plan['secoes'] if s['tipo'] != 'introducao']
        results = await asyncio.gather(*(self.section(plan, s) for s in development), return_exceptions=True)
        retry = []
        for s, result in zip(development, results):
            if isinstance(result, (Fatal, BudgetExceeded)):
                raise result
            if isinstance(result, BaseException):
                retry.append(s)
                self.summary['avisos'].append(f"{s['id']}: primeira tentativa falhou ({type(result).__name__}: {str(result)[:300]}); refazendo")
            else:
                done[s['id']] = result
        # Uma segunda passada para seções que falharam (as chamadas bem-sucedidas vêm do cache).
        for s in retry:
            try:
                done[s['id']] = await self.section(plan, s)
            except (Fatal, BudgetExceeded):
                raise
            except Exception as exc:
                self.fail(s['id'], exc)
        intro = plan['secoes'][0]
        neighbours = [dict(id=d['secao']['id'], titulo=d['secao']['titulo'],
                           subtitulos=[b['subtitulo'] for b in d['blocos']]) for d in done.values()]
        try:
            done[intro['id']] = await self.section(plan, intro, neighbours)
        except (Fatal, BudgetExceeded):
            raise
        except Exception as exc:
            self.fail(intro['id'], exc)
        self.stage('secoes', concluidas=len(done), planejadas=len(plan['secoes']))
        units = [u for d in done.values() for u in d['unidades']]
        document = self.assemble(plan, done)
        self.save('documento_rascunho.json', document)
        try:
            history = await self.consolidate_document(document)
        except (Fatal, BudgetExceeded):
            raise
        except Exception as exc:
            self.fail('consolidacao_documento', exc)
            history = []
        self.save('consolidacao_documento.json', history)
        self.stage('consolidacao_documento', rodadas=len(history))
        review, repairs = None, []
        try:
            review, repairs = await self.review_and_repair(document, done, units)
            self.save('revisao.json', dict(revisao=review, reparos=repairs))
        except (Fatal, BudgetExceeded):
            raise
        except Exception as exc:
            self.fail('revisao', exc)
        polish = None
        if self.cfg.get('polish', True):
            try:
                polish = await self.polish(document)
                self.save('polimento.json', polish)
                self.stage('polimento', **{k: polish[k] for k in ('antes', 'depois', 'blocos_alterados')})
            except (Fatal, BudgetExceeded):
                raise
            except Exception as exc:
                self.summary['avisos'].append('polimento não aplicado: ' + type(exc).__name__ + ': ' + str(exc)[:300])
        self.polish_info = polish and {k: polish[k] for k in ('antes', 'depois', 'blocos_alterados')} | dict(
            blocos_removidos=len(polish['blocos_removidos']), frases_de_enchimento_removidas=len(polish['enchimento_removido']))
        final_cov = None
        try:
            final_cov = await self.coverage(self.block_list(document), 'cobertura_final')
            self.save('cobertura_final.json', final_cov)
        except (Fatal, BudgetExceeded):
            raise
        except Exception as exc:
            self.fail('cobertura_final', exc)
        semantic = None
        spec = self.cfg.get('semantic')
        if spec and self.calls.transport is None:
            try:
                cache = self.folder / '.local' / 'embeddings.json'
                semantic = dict(antes=await S.redundancy(self.calls, T.clean(base_doc), spec, cache),
                                depois=await S.redundancy(self.calls, T.clean(document), spec, cache))
                S.compact(self.folder, spec, cache, {'antes': T.clean(base_doc), 'depois': T.clean(document)})
            except Exception as exc:  # medida auxiliar: não torna o documento parcial
                self.summary['avisos'].append('redundância semântica indisponível: ' + type(exc).__name__ + ': ' + str(exc)[:300])
        self.export(plan, done, document, units, history, review, repairs, base_doc, base_cov, final_cov, semantic)
        planned = len(plan['secoes'])
        complete = len(done) == planned and review is not None and final_cov is not None
        self.summary.update(status='concluido' if complete and not self.summary['falhas'] else 'parcial', fim=stamp())
        self.save('resumo.json', self.summary)
        (self.folder / 'RELATORIO.md').write_text(report(self.e, self.metrics, self.summary), encoding='utf-8')
        return self.summary

    def export_for_questions(self, document, units):
        """Blocos prontos para recorte: caminho, siglas do bloco expandidas e origem do conteúdo.

        Quem gerar questões a partir de qualquer recorte usa `para_questoes.contexto` para pôr
        à frente do trecho o documento, a seção e as siglas que aparecem nele."""
        glossary = getattr(self, 'glossary', None) or {}
        by_unit = {u['id']: u for u in units}
        rows = []
        for c in document['capitulos']:
            for b in c['blocos']:
                status = {}
                for u in b.get('unidades', []):
                    if u in by_unit:
                        status[by_unit[u]['estatuto']] = status.get(by_unit[u]['estatuto'], 0) + 1
                rows.append(dict(documento=self.e['id'], titulo_documento=self.e['titulo'], capitulo=c['titulo'],
                                 bloco=b['id'], subtitulo=b['subtitulo'], texto=b['texto'],
                                 siglas=_glossary_for(b['subtitulo'] + ' ' + b['texto'], glossary),
                                 unidades=b.get('unidades', []), estatuto=status,
                                 sem_evidencia=bool(status) and not set(status) & {'evidencia', 'base_revisada'},
                                 testabilidade=T.testability(dict(capitulos=[dict(blocos=[b])]))))
        (self.folder / 'blocos_questoes.jsonl').write_text(
            ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
        self.save('glossario.json', dict(sorted(glossary.items())))

    def export(self, plan, done, document, units, history, review, repairs, base_doc, base_cov, final_cov, semantic=None):
        final = T.clean(document)
        self.save('documento.json', final)
        (self.folder / 'documento.md').write_text(T.markdown(final), encoding='utf-8')
        self.save('documento_detalhado.json', document)
        passages = {pid: p for d in done.values() for pid, p in d['pesquisa']['passagens'].items()}
        self.save('proveniencia.json', dict(unidades=units, fontes={pid: public(p) for pid, p in passages.items()}))
        self.save('pesquisa.json', {sid: dict(rodadas=d['pesquisa']['rodadas'], achados=d['pesquisa']['achados'],
                                              verificacoes=d['pesquisa']['verificacoes'],
                                              lacunas_finais=d['pesquisa']['lacunas_finais'])
                                    for sid, d in done.items()})
        self.save('rascunhos.json', {sid: d['afirmacoes'] for sid, d in done.items()})
        self.save('consolidacao_secoes.json', {sid: d['consolidacao'] for sid, d in done.items()})
        metrics = measure(self.e, plan, done, base_doc, document, units, history, review, repairs, base_cov, final_cov,
                          self.cfg['redundancy_threshold'], self.calls.budget.used)
        metrics['semantica'] = semantic
        metrics['estilo'] = getattr(self, 'polish_info', None)
        metrics['testabilidade'] = dict(antes=T.testability(T.clean(base_doc)), depois=T.testability(final))
        self.export_for_questions(document, units)
        self.metrics = metrics
        self.save('metricas.json', metrics)
        (self.folder / 'RELATORIO.md').write_text(report(self.e, metrics, self.summary), encoding='utf-8')
        self.summary['metricas'] = {k: metrics[k] for k in ('antes', 'depois', 'cobertura', 'proveniencia')}


def _glossary_for(text, glossary):
    found = {T._base_sigla(m.group(0)) for m in T.SIGLA.finditer(text or '')}
    return {s: glossary[s] for s in sorted(found) if s in glossary}


def coverage_counts(cov, gaps):
    if not cov:
        return None
    counts = {'atendido': 0, 'parcial': 0, 'ausente': 0}
    for c in cov['cobertura']:
        counts[c['estado']] += 1
    n = max(1, len(gaps))
    return dict(counts, total=len(gaps), pct_atendido=round(100 * counts['atendido'] / n, 1),
                pct_atendido_ou_parcial=round(100 * (counts['atendido'] + counts['parcial']) / n, 1))


def measure(entrada, plan, done, base_doc, document, units, history, review, repairs, base_cov, final_cov, threshold, calls):
    gaps = gap_rows(entrada)
    before, after = T.clean(base_doc), T.clean(document)
    rb, ra = T.redundancy(before, threshold), T.redundancy(after, threshold)
    status = {}
    for u in units:
        status[u['estatuto']] = status.get(u['estatuto'], 0) + 1
    claims = sum(len(d['afirmacoes']) for d in done.values())
    discarded = {}
    for d in done.values():
        for x in d['consolidacao'].get('descartadas', []):
            discarded[x['motivo']] = discarded.get(x['motivo'], 0) + 1
    passages = {pid: p for d in done.values() for pid, p in d['pesquisa']['passagens'].items()}
    cited = {pid for u in units for pid in u['fontes']}
    collections = {}
    for pid in cited:
        col = passages[pid].get('collection') if pid in passages else None
        collections[col] = collections.get(col, 0) + 1
    verif = {'apoia': 0, 'contradiz': 0}
    for d in done.values():
        for vs in d['pesquisa']['verificacoes'].values():
            for v in vs:
                verif[v['estado']] += 1
    lint_final = T.lint(' '.join(b['subtitulo'] + ' ' + b['texto'] for c in after['capitulos'] for b in c['blocos']))
    side = lambda doc, red: dict(**T.stats(doc), taxa_redundancia=red['taxa_redundancia'],
                                 pares_redundantes=red['n_pares'], similaridade_maxima_media=red['similaridade_maxima_media'],
                                 repeticao_6gramas=red['repeticao_6gramas'])
    return dict(schema=VERSION, item=entrada['id'], antes=side(before, rb), depois=side(after, ra),
        cobertura=dict(antes=coverage_counts(base_cov, gaps), depois=coverage_counts(final_cov, gaps),
                       lacunas_fora_de_escopo=[x['id'] for x in plan.get('lacunas_fora_de_escopo', [])]),
        proveniencia=dict(unidades=len(units), por_estatuto=status,
                          pct_com_evidencia=round(100 * status.get('evidencia', 0) / max(1, len(units)), 1)),
        rascunhos=dict(afirmacoes=claims, unidades=len(units), fusao=round(claims / max(1, len(units)), 2),
                       descartadas_por_motivo=discarded,
                       sem_destino_explicito=sum(len(d['consolidacao'].get('nao_contabilizadas', [])) for d in done.values())),
        pesquisa=dict(rodadas=sum(len(d['pesquisa']['rodadas']) for d in done.values()), passagens_lidas=len(passages),
                      passagens_citadas=len(cited), colecoes_citadas=collections,
                      achados=sum(len(d['pesquisa']['achados']) for d in done.values()), verificacoes=verif),
        roteiro=dict(secoes=len(plan['secoes']), concluidas=len(done),
                     blocos_base_reaproveitados=sum(len(s['blocos_base']) for s in plan['secoes']),
                     blocos_base_descartados=len(plan.get('blocos_descartados', []))),
        consolidacao_documento=[{k: h.get(k) for k in ('rodada', 'pares_internos', 'pares_entre_documentos', 'taxa_antes', 'taxa_depois')}
                                | dict(operacoes=len(h.get('operacoes', []))) for h in history],
        revisao=dict(problemas=len(review['problemas']) if review else None, reparos=len(repairs),
                     problemas_por_tipo=_count(review['problemas'], 'tipo') if review else {}),
        alertas_locais_finais=len(lint_final), chamadas_reservadas=calls)


def _count(rows, key):
    out = {}
    for r in rows:
        out[r[key]] = out.get(r[key], 0) + 1
    return out


def report(entrada, m, summary):
    a, d = m['antes'], m['depois']
    ca, cd = m['cobertura']['antes'], m['cobertura']['depois']
    fmt = lambda c: '-' if not c else f"{c['atendido']}/{c['total']} atendidas, {c['parcial']} parciais ({c['pct_atendido']}%)"
    lines = [f"# Refino: {entrada['titulo']}", '', f"**Estado:** {summary['status']}", '',
             '| Medida | Base revisada | Nova versão |', '|---|---|---|',
             f"| Palavras | {a['palavras']} | {d['palavras']} |", f"| Blocos | {a['blocos']} | {d['blocos']} |",
             f"| Sentenças com quase-duplicata | {a['taxa_redundancia']:.1%} | {d['taxa_redundancia']:.1%} |",
             f"| Repetição de 6-gramas | {a['repeticao_6gramas']:.1%} | {d['repeticao_6gramas']:.1%} |",
             f"| Lacunas do especialista | {fmt(ca)} | {fmt(cd)} |"]
    if m.get('semantica'):
        sa, sd = m['semantica']['antes'], m['semantica']['depois']
        lines.append(f"| Sentenças com paráfrase em outro bloco (embeddings ≥ {sa['limiar']}) | "
                     f"{sa['taxa_redundancia_semantica']:.1%} | {sd['taxa_redundancia_semantica']:.1%} |")
    lines += ['',
             f"Unidades de conteúdo: {m['proveniencia']['unidades']} ({m['proveniencia']['por_estatuto']}); "
             f"{m['proveniencia']['pct_com_evidencia']}% com evidência nos corpora.",
             f"Rascunhos: {m['rascunhos']['afirmacoes']} afirmações fundidas em {m['rascunhos']['unidades']} unidades; "
             f"descartes {m['rascunhos']['descartadas_por_motivo']}.",
             f"Pesquisa: {m['pesquisa']['rodadas']} rodadas, {m['pesquisa']['passagens_lidas']} passagens lidas, "
             f"{m['pesquisa']['passagens_citadas']} citadas, por coleção {m['pesquisa']['colecoes_citadas']}.",
             f"Revisão: {m['revisao']['problemas']} problemas, {m['revisao']['reparos']} blocos reparados; "
             f"alertas locais finais: {m['alertas_locais_finais']}. Chamadas reservadas: {m['chamadas_reservadas']}.", '']
    if m.get('testabilidade'):
        ta, td = m['testabilidade']['antes'], m['testabilidade']['depois']
        lines[-1:-1] = [f"Uso como fonte de questões: sentenças com relação verificável {ta['testaveis']:.0%} → {td['testaveis']:.0%}; "
                        f"sentenças vagas {ta['vagas']:.0%} → {td['vagas']:.0%}."]
    if m.get('estilo'):
        e = m['estilo']
        lines[-1:-1] = [f"Polimento de estilo: {e['blocos_alterados']} blocos ajustados, {e['blocos_removidos']} removidos, "
                        f"{e.get('frases_de_enchimento_removidas', 0)} frases de enchimento cortadas; "
                        f"antes {e['antes']}, depois {e['depois']}."]
    if summary['falhas']:
        lines += ['## Falhas', ''] + [f"- {f['etapa']}: {f['erro']}" for f in summary['falhas']] + ['']
    lines += ['Arquivos: documento.md (nova versão), documento_base.md (base revisada), roteiro.json, rascunhos.json,',
              'pesquisa.json, consolidacao_secoes.json, proveniencia.json, consolidacao_documento.json, revisao.json, metricas.json.']
    return '\n'.join(lines) + '\n'
