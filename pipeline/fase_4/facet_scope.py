"""Facetas com termos específicos e escopo de aplicação preservado."""
SYSTEM_ADDITION='''Nesta execução QA o escopo é FPSO/FSO e suas interfaces de produção subsea. Concretize cada faceta em objetivos profissionais delimitados pelo escopo fornecido; não exija simultaneamente todos os aspectos do subtópico em uma faceta. Inclua aplicação FPSO/offshore nas queries sem exigir nome de uma unidade específica. KPI, gestão, metas, desempenho, programação, projeto e suas traduções isoladas não são termos fortes: use-os como apoio. Busque expressões técnicas distintivas do recorte, como disponibilidade operacional, perda de produção, manutenção em atraso, planejamento da manutenção ou elementos críticos, somente quando previstos na instrução. Princípios transferíveis precisam de condições sustentadas, sem assumir arranjo de refinaria, estudo particular ou modelo de maturidade como configuração de FPSO.'''
GENERIC_TERMS={'kpi','gestao','indicador','indicadores','metas','meta','desempenho','programacao','projeto',
               'performance','management','indicator','indicators','project','planning',
               'key performance indicator','key performance indicators','performance indicator','performance indicators'}


def generic_term(text):
    import unicodedata
    plain=''.join(c for c in unicodedata.normalize('NFKD',text.casefold().strip()) if not unicodedata.combining(c))
    return plain in GENERIC_TERMS


class ScopedFacetClient:
    def __init__(self,client):self.client=client
    def complete_json(self,prompt,**kwargs):
        kwargs['system']=kwargs.get('system','')+'\n'+SYSTEM_ADDITION
        result=self.client.complete_json(prompt,**kwargs)
        if isinstance(result,dict):
            for facet in result.get('facetas',[]):
                if not isinstance(facet,dict):continue
                strong=facet.get('termos_fortes',[]);support=facet.get('termos_apoio',[])
                if not isinstance(strong,list) or not isinstance(support,list):continue
                moved=[t for t in strong if isinstance(t,str) and generic_term(t)]
                facet['termos_fortes']=[t for t in strong if t not in moved]
                facet['termos_apoio']=list(dict.fromkeys(support+moved))
        return result
