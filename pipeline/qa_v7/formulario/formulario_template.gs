/**
 * PetroQuest: formulário de avaliação de questões por especialista (Google Apps Script).
 *
 * Como usar:
 *   1. Acesse https://script.google.com, crie um projeto novo e cole este arquivo inteiro no Código.gs.
 *   2. Selecione a função criarFormulario e clique em Executar. Autorize o acesso ao Google Forms/Sheets.
 *   3. O script cria o formulário (e a planilha de respostas). Se o registro de execução disser que pausou
 *      por tempo, execute criarFormulario de novo: ele continua de onde parou.
 *   4. No final, o registro mostra o link para editar e o link para enviar ao especialista (listarLinks
 *      mostra de novo). Para começar do zero, execute recomecar e depois criarFormulario.
 *
 * Cada questão ocupa uma página: enunciado, resposta, 4 notas de 1 a 5, o contexto usado na geração
 * com parecer e motivo, e o parecer final da questão com motivo. Os títulos levam o código (Q001...)
 * para cruzar as respostas com o arquivo mapa_questoes_formulario.csv.
 */

const CONFIG = {
  titulo: 'PetroQuest: avaliação de questões por especialista',
  // true: um formulário por tópico (o especialista envia por partes). false: um formulário único.
  umFormularioPorTopico: false,
  criarPlanilhaDeRespostas: true,
  permitirEditarResposta: true,
};

const CRITERIOS = [
  'Clareza do enunciado',
  'Corretude técnica',
  'Relevância para a operação de FPSOs',
  'Qualidade da resposta correta',
];
const PARECERES = ['Aprovado', 'Aprovado com ressalvas', 'Rejeitado'];
const LIMITE_MS = 5 * 60 * 1000;  // o Apps Script encerra execuções com 6 minutos

const QUESTOES = /*__QUESTOES__*/[];

function criarFormulario() {
  const inicio = Date.now();
  const props = PropertiesService.getScriptProperties();
  let estado = JSON.parse(props.getProperty('ESTADO') || 'null');
  if (!estado) {
    estado = { grupos: montarGrupos_(), atual: 0 };
  }
  while (estado.atual < estado.grupos.length) {
    const grupo = estado.grupos[estado.atual];
    const form = grupo.formId ? FormApp.openById(grupo.formId) : novoFormulario_(grupo, props, estado);
    grupo.formId = form.getId();
    while (grupo.proxima < grupo.questoes.length) {
      if (Date.now() - inicio > LIMITE_MS) {
        props.setProperty('ESTADO', JSON.stringify(estado));
        Logger.log('Pausado por tempo: %s questões criadas em "%s". Execute criarFormulario de novo para continuar.',
                   grupo.proxima, grupo.titulo);
        return;
      }
      const q = QUESTOES[grupo.questoes[grupo.proxima]];
      adicionarQuestao_(form, q, grupo.proxima + 1, grupo.questoes.length);
      grupo.proxima += 1;
      props.setProperty('ESTADO', JSON.stringify(estado));
    }
    estado.atual += 1;
    props.setProperty('ESTADO', JSON.stringify(estado));
  }
  Logger.log('Concluído: %s questões.', QUESTOES.length);
  listarLinks();
}

function listarLinks() {
  const estado = JSON.parse(PropertiesService.getScriptProperties().getProperty('ESTADO') || 'null');
  if (!estado) {
    Logger.log('Nenhum formulário criado ainda. Execute criarFormulario.');
    return;
  }
  estado.grupos.forEach(function (g) {
    if (!g.formId) return;
    const form = FormApp.openById(g.formId);
    Logger.log('%s\n  Para o especialista: %s\n  Para editar: %s\n  Questões criadas: %s de %s',
               g.titulo, form.getPublishedUrl(), form.getEditUrl(), g.proxima, g.questoes.length);
  });
}

function recomecar() {
  PropertiesService.getScriptProperties().deleteProperty('ESTADO');
  Logger.log('Estado apagado. Os formulários já criados continuam no seu Google Drive.');
}

function montarGrupos_() {
  if (!CONFIG.umFormularioPorTopico) {
    return [{ titulo: CONFIG.titulo, questoes: QUESTOES.map(function (_, i) { return i; }), proxima: 0, formId: null }];
  }
  const grupos = [];
  const porTopico = {};
  QUESTOES.forEach(function (q, i) {
    if (!(q.topico in porTopico)) {
      porTopico[q.topico] = grupos.length;
      grupos.push({ titulo: CONFIG.titulo + ': ' + q.topico, questoes: [], proxima: 0, formId: null });
    }
    grupos[porTopico[q.topico]].questoes.push(i);
  });
  return grupos;
}

function novoFormulario_(grupo, props, estado) {
  const form = FormApp.create(grupo.titulo);
  grupo.formId = form.getId();
  props.setProperty('ESTADO', JSON.stringify(estado));  // guarda o id antes de qualquer outra chamada
  form.setDescription(
    'Obrigado por colaborar. Cada página traz uma questão gerada automaticamente sobre operação de FPSOs, ' +
    'com a resposta considerada correta. Avalie a questão com notas de 1 (muito ruim) a 5 (excelente), ' +
    'depois avalie o contexto usado para gerá-la e, por fim, dê o parecer sobre a questão.\n\n' +
    'Quando marcar "Rejeitado" ou "Aprovado com ressalvas", escreva o motivo no campo logo abaixo. ' +
    'Sugestões de correção são muito bem-vindas.\n\n' +
    'Questões: ' + grupo.questoes.length + '. ' +
    (CONFIG.permitirEditarResposta ? 'Depois de enviar, você poderá editar suas respostas pelo link de edição.' : ''));
  form.setProgressBar(true);
  form.setCollectEmail(false);
  form.setAllowResponseEdits(CONFIG.permitirEditarResposta);
  form.setShuffleQuestions(false);
  form.addTextItem().setTitle('Nome completo').setRequired(true);
  const email = form.addTextItem().setTitle('E-mail').setRequired(true);
  email.setValidation(FormApp.createTextValidation().requireTextIsEmail()
    .setHelpText('Informe um e-mail válido.').build());
  if (CONFIG.criarPlanilhaDeRespostas) {
    const planilha = SpreadsheetApp.create(grupo.titulo + ' (respostas)');
    form.setDestination(FormApp.DestinationType.SPREADSHEET, planilha.getId());
  }
  return form;
}

function adicionarQuestao_(form, q, n, total) {
  const c = q.codigo;
  form.addPageBreakItem()
    .setTitle(c + ' · Questão ' + n + ' de ' + total)
    .setHelpText('Tópico: ' + q.topico + '\nSubtópico: ' + q.subtopico + '\nNível pretendido: ' + q.nivel);
  form.addSectionHeaderItem().setTitle('Enunciado').setHelpText(q.pergunta);
  form.addSectionHeaderItem().setTitle('Resposta correta').setHelpText(q.resposta);
  CRITERIOS.forEach(function (criterio) {
    form.addScaleItem()
      .setTitle(c + ' · ' + criterio)
      .setBounds(1, 5)
      .setLabels('Muito ruim', 'Excelente')
      .setRequired(true);
  });
  form.addSectionHeaderItem()
    .setTitle('Contexto usado para gerar a questão')
    .setHelpText(q.contexto);
  form.addMultipleChoiceItem()
    .setTitle(c + ' · Parecer sobre o contexto')
    .setHelpText('O material é tecnicamente correto e adequado para sustentar esta questão?')
    .setChoiceValues(PARECERES)
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle(c + ' · Motivo (contexto)')
    .setHelpText('Obrigatório se marcou "Rejeitado" ou "Aprovado com ressalvas".');
  form.addMultipleChoiceItem()
    .setTitle(c + ' · Parecer final sobre a questão')
    .setChoiceValues(PARECERES)
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle(c + ' · Motivo (questão)')
    .setHelpText('Obrigatório se marcou "Rejeitado" ou "Aprovado com ressalvas". Se possível, sugira a correção.');
}
