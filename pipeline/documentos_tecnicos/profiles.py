"""Perfis guiam a leitura; não certificam uma coleção nem bloqueiam gêneros por nome."""

PROFILES = {
    'regis': 'REGIS: coleção de recuperação de informação. Diferencie explicação técnica, entrevista, '
             'opinião, hipótese e resultado experimental. Depoimento de especialista não é consenso. '
             'Verifique fundamento e condições. Não confunda relevância de busca com verdade.',
    'petroles': 'Petrolês: pode conter números mascarados e publicações concatenadas sem fronteiras '
                'confiáveis. Não reconstrua valores, equações, autoria ou continuidade entre documentos. '
                'Use apenas relações compreensíveis e sustentadas pelo texto disponível.',
    'anp': 'ANP: diferencie descrição de instalação, depoimento, conclusão de investigação, '
           'recomendação e requisito normativo. Evento observado não prova mecanismo universal. '
           'Identifique escopo e versão antes de formular obrigação.',
    'hse': 'HSE: identifique se o documento é orientação, guia de inspeção ou referência regulatória. '
           'Contexto britânico não constitui automaticamente obrigação brasileira. Um princípio '
           'de engenharia pode ser transferível se as condições técnicas forem compatíveis.',
    'bsee': 'BSEE: diferencie incidente, recomendação preventiva e requisito dos EUA. Preserve '
            'condições do sistema/atividade. Não trate ocorrência isolada como frequência geral '
            'nem recomendação como norma brasileira.',
}


def annotate(evidence):
    collection = evidence.get('metadados', {}).get('collection') or ''
    return {**evidence, 'orientacao_leitura': PROFILES.get(collection.casefold(),
            'Origem sem perfil específico: examine gênero, autoria, evidência, escopo e limitações.')}
