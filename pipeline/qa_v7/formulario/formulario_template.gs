/**
 * PetroQuest: formulários de avaliação de questões por especialista (Google Apps Script).
 *
 * Como usar:
 *   1. Acesse https://script.google.com, crie um projeto novo e cole este arquivo inteiro no Código.gs.
 *   2. Selecione a função criarFormulario e clique em Executar. Autorize o acesso ao Google Forms/Sheets.
 *   3. Se o registro de execução disser que pausou por tempo, execute criarFormulario de novo:
 *      ele continua de onde parou, sem duplicar.
 *   4. No final, o registro mostra os links (listarLinks mostra de novo).
 *      Para começar do zero, execute recomecar, apague os formulários antigos no Drive e rode criarFormulario.
 *
 * Por padrão é criado um formulário por tópico (10 questões cada): o Google Forms limita o número de itens
 * por formulário e 100 questões numa página só ficariam longas demais para uma sessão. Se mesmo assim um
 * formulário atingir o limite, o script cria automaticamente uma "parte 2" e continua dali.
 *
 * Cada questão ocupa uma página: enunciado, resposta, grade de notas de 1 a 5, o contexto usado na geração
 * com parecer e motivo, e o parecer final da questão com motivo. Os títulos levam o código (Q001...) para
 * cruzar as respostas com o arquivo mapa_questoes_formulario.csv.
 */

const CONFIG = {
  titulo: 'PetroQuest: avaliação de questões por especialista',
  // true: um formulário por tópico (recomendado). false: tenta um formulário único (divide em partes se lotar).
  umFormularioPorTopico: true,
  criarPlanilhaDeRespostas: true,
  permitirEditarResposta: true,
};

const CRITERIOS = [
  'Clareza do enunciado',
  'Corretude técnica',
  'Relevância para a operação de FPSOs',
  'Qualidade da resposta correta',
];
const NOTAS = ['1 (muito ruim)', '2', '3', '4', '5 (excelente)'];
const PARECERES = ['Aprovado', 'Aprovado com ressalvas', 'Rejeitado'];
const LIMITE_MS = 5 * 60 * 1000;  // o Apps Script encerra execuções com 6 minutos

const QUESTOES = /*__QUESTOES__*/[];

function criarFormulario() {
  const inicio = Date.now();
  const props = PropertiesService.getScriptProperties();
  let estado = JSON.parse(props.getProperty('ESTADO') || 'null');
  if (!estado || !estado.versao) {
    estado = { versao: 2, grupos: montarGrupos_(), atual: 0 };
  }
  const salvar = function () { props.setProperty('ESTADO', JSON.stringify(estado)); };
  while (estado.atual < estado.grupos.length) {
    const grupo = estado.grupos[estado.atual];
    if (!grupo.formIds.length) {
      novoFormulario_(grupo, salvar);
    }
    let form = FormApp.openById(grupo.formIds[grupo.formIds.length - 1]);
    let vazio = grupo.formIds.length > 1 && grupo.inicioParte === grupo.proxima;
    while (grupo.proxima < grupo.questoes.length) {
      if (Date.now() - inicio > LIMITE_MS) {
        salvar();
        Logger.log('Pausado por tempo: %s de %s questões criadas em "%s". Execute criarFormulario de novo.',
                   grupo.proxima, grupo.questoes.length, grupo.titulo);
        return;
      }
      const q = QUESTOES[grupo.questoes[grupo.proxima]];
      if (adicionarQuestao_(form, q, grupo.proxima + 1, grupo.questoes.length)) {
        grupo.proxima += 1;
        vazio = false;
        salvar();
        continue;
      }
      if (vazio) {
        throw new Error('Um formulário novo não comportou nem uma questão: limite de itens inesperado.');
      }
      Logger.log('"%s" atingiu o limite de itens na questão %s. Criando uma nova parte.', grupo.titulo, q.codigo);
      grupo.inicioParte = grupo.proxima;
      form = novoFormulario_(grupo, salvar);
      vazio = true;
    }
    estado.atual += 1;
    salvar();
  }
  Logger.log('Concluído: %s questões.', QUESTOES.length);
  listarLinks();
}

function listarLinks() {
  const estado = JSON.parse(PropertiesService.getScriptProperties().getProperty('ESTADO') || 'null');
  if (!estado || !estado.versao) {
    Logger.log('Nenhum formulário criado ainda. Execute criarFormulario.');
    return;
  }
  estado.grupos.forEach(function (g) {
    g.formIds.forEach(function (id, i) {
      const form = FormApp.openById(id);
      Logger.log('%s%s\n  Para o especialista: %s\n  Para editar: %s',
                 g.titulo, g.formIds.length > 1 ? ' (parte ' + (i + 1) + ')' : '',
                 form.getPublishedUrl(), form.getEditUrl());
    });
    Logger.log('  Questões criadas: %s de %s', g.proxima, g.questoes.length);
  });
}

function recomecar() {
  PropertiesService.getScriptProperties().deleteProperty('ESTADO');
  Logger.log('Estado apagado. Os formulários já criados continuam no seu Google Drive; apague-os se não forem usar.');
}

function montarGrupos_() {
  const novo = function (titulo) { return { titulo: titulo, questoes: [], proxima: 0, formIds: [], inicioParte: 0 }; };
  if (!CONFIG.umFormularioPorTopico) {
    const g = novo(CONFIG.titulo);
    QUESTOES.forEach(function (_, i) { g.questoes.push(i); });
    return [g];
  }
  const grupos = [];
  const porTopico = {};
  QUESTOES.forEach(function (q, i) {
    if (!(q.topico in porTopico)) {
      porTopico[q.topico] = grupos.length;
      grupos.push(novo(CONFIG.titulo + ': ' + q.topico));
    }
    grupos[porTopico[q.topico]].questoes.push(i);
  });
  return grupos;
}

function novoFormulario_(grupo, salvar) {
  const parte = grupo.formIds.length + 1;
  const titulo = grupo.titulo + (parte > 1 ? ' (parte ' + parte + ')' : '');
  const form = FormApp.create(titulo);
  grupo.formIds.push(form.getId());
  salvar();  // guarda o id antes de qualquer outra chamada
  form.setDescription(
    'Obrigado por colaborar. Cada página traz uma questão gerada automaticamente sobre operação de FPSOs, ' +
    'com a resposta considerada correta. Dê notas de 1 (muito ruim) a 5 (excelente) aos quatro critérios, ' +
    'avalie o contexto usado para gerar a questão e, por fim, dê o parecer sobre a questão.\n\n' +
    'Quando marcar "Rejeitado" ou "Aprovado com ressalvas", escreva o motivo no campo logo abaixo. ' +
    'Sugestões de correção são muito bem-vindas.' +
    (CONFIG.permitirEditarResposta ? '\n\nDepois de enviar, você poderá editar suas respostas pelo link de edição.' : ''));
  form.setProgressBar(true);
  form.setCollectEmail(false);
  form.setAllowResponseEdits(CONFIG.permitirEditarResposta);
  form.setShuffleQuestions(false);
  form.addTextItem().setTitle('Nome completo').setRequired(true);
  const email = form.addTextItem().setTitle('E-mail').setRequired(true);
  email.setValidation(FormApp.createTextValidation().requireTextIsEmail()
    .setHelpText('Informe um e-mail válido.').build());
  if (CONFIG.criarPlanilhaDeRespostas) {
    const planilha = SpreadsheetApp.create(titulo + ' (respostas)');
    form.setDestination(FormApp.DestinationType.SPREADSHEET, planilha.getId());
  }
  return form;
}

/** Cria a página da questão. Devolve false (sem deixar itens soltos) se o formulário atingiu o limite. */
function adicionarQuestao_(form, q, n, total) {
  const criados = [];
  const add = function (item) { criados.push(item); return item; };
  const c = q.codigo;
  try {
    add(form.addPageBreakItem())
      .setTitle(c + ' · Questão ' + n + ' de ' + total)
      .setHelpText('Tópico: ' + q.topico + '\nSubtópico: ' + q.subtopico + '\nNível pretendido: ' + q.nivel);
    add(form.addSectionHeaderItem()).setTitle('Enunciado').setHelpText(q.pergunta);
    add(form.addSectionHeaderItem()).setTitle('Resposta correta').setHelpText(q.resposta);
    add(form.addGridItem())
      .setTitle(c + ' · Notas da questão')
      .setHelpText('De 1 (muito ruim) a 5 (excelente), uma nota por linha.')
      .setRows(CRITERIOS)
      .setColumns(NOTAS)
      .setRequired(true);
    add(form.addSectionHeaderItem())
      .setTitle('Contexto usado para gerar a questão')
      .setHelpText(q.contexto);
    add(form.addMultipleChoiceItem())
      .setTitle(c + ' · Parecer sobre o contexto')
      .setHelpText('O material é tecnicamente correto e adequado para sustentar esta questão?')
      .setChoiceValues(PARECERES)
      .setRequired(true);
    add(form.addParagraphTextItem())
      .setTitle(c + ' · Motivo (contexto)')
      .setHelpText('Obrigatório se marcou "Rejeitado" ou "Aprovado com ressalvas".');
    add(form.addMultipleChoiceItem())
      .setTitle(c + ' · Parecer final sobre a questão')
      .setChoiceValues(PARECERES)
      .setRequired(true);
    add(form.addParagraphTextItem())
      .setTitle(c + ' · Motivo (questão)')
      .setHelpText('Obrigatório se marcou "Rejeitado" ou "Aprovado com ressalvas". Se possível, sugira a correção.');
    return true;
  } catch (e) {
    criados.reverse().forEach(function (item) {
      try { form.deleteItem(item); } catch (ignorado) { /* item já inexistente */ }
    });
    if (/m[áa]ximo de itens|maximum number of items|too many items/i.test(String(e && e.message || e))) {
      return false;
    }
    throw e;
  }
}
