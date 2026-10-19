"""Orientações de leitura apresentadas uma vez por coleção em cada chamada."""

PROFILES = {
    'regis': """Examine o gênero e a fundamentação de cada passagem. Diferencie explicação técnica,
resultado de estudo, hipótese e opinião. Uma entrevista pode conter conhecimento útil;
um depoimento isolado não estabelece consenso nem regra geral.""",
    'petroles': """Considere as limitações da extração: podem existir números mascarados, referências
ausentes e publicações concatenadas sem fronteiras confiáveis. Use as informações
que permanecem compreensíveis, preservando lacunas de valores, autoria e continuidade.""",
    'anp': """Diferencie descrição de instalação, depoimento, conclusão de investigação, recomendação
e requisito. Preserve o alcance do caso e a condição das conclusões. Obrigações exigem
referência, escopo e versão aplicáveis.""",
    'hse': """Identifique se o material é orientação técnica, guia de inspeção ou referência regulatória.
Examine as condições de aplicação dos princípios de engenharia. Mantenha explícito
quando uma exigência depende do contexto britânico.""",
    'bsee': """Diferencie ocorrência relatada, recomendação preventiva e requisito. Preserve o sistema,
a atividade e as condições descritas. Mantenha explícito quando uma exigência depende
do contexto regulatório dos Estados Unidos.""",
}


def source_context(evidences):
    """Preserva trechos e proveniência; separa a orientação comum da coleção."""
    sources, profiles = [], {}
    for evidence in evidences:
        sources.append({k: v for k, v in evidence.items() if k != 'orientacao_leitura'})
        collection = evidence.get('metadados', {}).get('collection') or ''
        key = collection.casefold()
        profiles.setdefault(key, {'colecao': collection or 'origem desconhecida',
                                  'orientacao': PROFILES.get(key,
                                      'Examine gênero, autoria, fundamento, escopo e limitações.')})
    return {'fontes_originais': sources, 'orientacoes_corpus': list(profiles.values())}
