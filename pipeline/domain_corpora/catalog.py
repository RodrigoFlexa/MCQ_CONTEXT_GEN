"""Pontos oficiais de descoberta; somente coleções aprovadas pelo usuário."""
ANP_ROOT = 'https://www.gov.br/anp/pt-br/assuntos/exploracao-e-producao-de-oleo-e-gas/seguranca-operacional'
ANP_INCIDENTS = ANP_ROOT + '/incidentes/relatorios-de-investigacao-de-incidentes-1/relatorios-de-investigacao-de-incidentes'
BSEE_INDEX = 'https://www.bsee.gov/guidance-and-regulations/guidance/safety-alerts-program'
REGIS_RECORD = 'https://zenodo.org/api/records/4726013'
SOURCES = {
    'anp': {'language':'pt', 'jurisdiction':'BR', 'landing':ANP_INCIDENTS,
            'license':'public_access; verificar direitos no documento'},
    'hse': {'language':'en', 'jurisdiction':'UK', 'landing':'https://www.hse.gov.uk/offshore/resources.htm',
            'license':'OGL-3.0 salvo exceções indicadas; https://www.hse.gov.uk/copyright.htm'},
    'bsee': {'language':'en', 'jurisdiction':'US', 'landing':BSEE_INDEX,
             'license':'public_access; verificar direitos de terceiros no documento'},
    'regis': {'language':'pt', 'jurisdiction':'not_specified', 'landing':'https://zenodo.org/records/4726013',
              'license':'other-open conforme Zenodo; não inferir licença dos documentos pela licença do código'},
}
# PDFs ligados nas páginas oficiais. Permitem continuar quando uma página HTML
# estiver indisponível; falhas de descoberta continuam explícitas no relatório.
DIRECT = {
    'anp': [ANP_ROOT+'/arq/raso/2023-relatorio-anual-seguranca-operacional.pdf/@@download/file'],
    'hse': ['https://www.hse.gov.uk/offshore/assets/docs/'+name+'.pdf' for name in (
        'kp3','inspection-of-loss-of-containment','ed-cyber-security',
        'ed-loss-of-stability-and-positioning','ed-maintenance-management',
        'ed-operational-risk-assessment','ed-audit-monitoring-review','ed-control-of-work',
        'ed-evacuation-escape-rescue','ed-active-fire-protection',
        'ed-offshore-inspection-guide-marine-operations','pipelines-integrity-management-inspection',
        'ed-sece-management-and-verification','structural-integrity-inspection-guide',
        'ed-temporary-refuge-integrity','ed-well-control','ed-well-integrity')],
    'bsee': ['https://www.bsee.gov/sites/bsee.gov/files/safety-alerts/safety/sa-301.pdf'],
}
INDEXES = {
    'anp': [ANP_INCIDENTS, ANP_ROOT],
    'hse': ['https://www.hse.gov.uk/offshore/'+s for s in (
        'inspection.htm','programmereports.htm','resources.htm','topics.htm','infosheets.htm','notices/')],
    'bsee': [BSEE_INDEX],
}
