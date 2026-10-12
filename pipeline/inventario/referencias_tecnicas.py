"""Guia técnico compartilhado pelo redator e pelo revisor; sem busca automática."""
import re

REFERENCES = {
    'nist_taxa_falha': {
        'url': 'https://www.itl.nist.gov/div898/handbook/apr/section1/apr123.htm',
        'conteudo': 'Para populações não reparáveis e tempo até falha, h(t)=f(t)/R(t) é taxa instantânea condicional por unidade de tempo. '
                    'Não é a probabilidade acumulada de falhar até t.'},
    'nist_sobrevivencia': {
        'url': 'https://www.itl.nist.gov/div898/handbook/apr/section1/apr122.htm',
        'conteudo': 'F(t) é a probabilidade acumulada de falha até t; R(t)=1-F(t) é a probabilidade de sobreviver além de t.'},
    'nist_ocorrencia_falhas': {
        'url': 'https://www.itl.nist.gov/div898/handbook/apr/section1/apr125.htm',
        'conteudo': 'Para sistemas reparáveis, a taxa de ocorrência de falhas (ROCOF) é a taxa média de eventos '
                    'por unidade de tempo, derivada do número esperado de falhas acumuladas. Não é uma probabilidade '
                    'nem o tempo de reparo. Distinguir esta modelagem da taxa instantânea de tempo até falha.'},
    'hse_passagem_servico': {
        'url':'https://www.hse.gov.uk/humanfactors/topics/shift-handover.htm',
        'conteudo':'A passagem de serviço comunica informação relevante à tarefa de modo preciso e confiável. '
                   'Inclui preparação de quem entrega, troca de informação e conferência por quem assume a responsabilidade. '
                   'Essa orientação de fatores humanos não é apresentada como obrigação da ANP.'},
}

BASES = ('fonte_original', 'referencia_tecnica', 'normalizacao_tecnica_modelo')

def numbers(text):
    return set(re.findall(r'\d+(?:[.,]\d+)*', text))
