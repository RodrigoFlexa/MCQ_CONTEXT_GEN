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
 * Por padrão é criado um formulário por tópico (5 questões cada): o Google Forms limita o número de itens
 * por formulário e 100 questões numa página só ficariam longas demais para uma sessão. Se mesmo assim um
 * formulário atingir o limite, o script cria automaticamente uma "parte 2" e continua dali.
 *
 * Cada questão ocupa uma página: enunciado, resposta, critério de correção, justificativa, grade de notas de 1 a 5, o contexto usado na geração
 * com parecer e motivo, o parecer final da questão com motivo e a concordância com a nossa classificação de
 * dificuldade. Quem discorda vai para uma página curta: a classificação que daria e os motivos (com "Outro"). Os títulos levam o código (Q001...) para
 * cruzar as respostas com o arquivo mapa_questoes_formulario.csv.
 */

const CONFIG = {
  titulo: 'PetroQuest: avaliação de questões por especialista',
  // true: um formulário por tópico (recomendado). false: tenta um formulário único (divide em partes se lotar).
  umFormularioPorTopico: true,
  criarPlanilhaDeRespostas: true,
  permitirEditarResposta: false,  // o especialista só avalia; não edita a resposta depois de enviar
};

const CRITERIOS = [
  'Clareza do enunciado',
  'Corretude técnica',
  'Relevância para a operação de FPSOs',
  'Qualidade da resposta correta',
];
const NOTAS = ['1 (muito ruim)', '2', '3', '4', '5 (excelente)'];
const PARECERES = ['Aprovado', 'Aprovado com ressalvas', 'Rejeitado'];
const NIVEIS = ['Fácil', 'Média', 'Difícil'];
const CONCORDO = 'Concordo';
const DISCORDO = 'Discordo';
const MOTIVOS_DIFICULDADE = [
  'Exige apenas recordar um conceito ou definição',
  'A resposta é direta ou está sugerida no próprio enunciado',
  'É conhecimento básico para quem atua em FPSO',
  'O cenário não acrescenta raciocínio; a decisão é direta',
  'Exige integrar vários conceitos, sistemas ou disciplinas',
  'Exige várias etapas de raciocínio ou análise de prós e contras',
  'Exige conhecimento especializado ou pouco difundido',
  'Exige experiência prática de operação',
  'Envolve cálculo ou interpretação de valores e dados',
];
const LIMITE_MS = 5 * 60 * 1000;  // o Apps Script encerra execuções com 6 minutos

const QUESTOES = /*__QUESTOES__*/[];

function criarFormulario() {
  const inicio = Date.now();
  const props = PropertiesService.getScriptProperties();
  let estado = JSON.parse(props.getProperty('ESTADO') || 'null');
  if (!estado || estado.versao !== 4) {
    estado = { versao: 4, grupos: montarGrupos_(), atual: 0 };
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
      const criada = adicionarQuestao_(form, q, grupo.proxima + 1, grupo.questoes.length);
      if (criada) {
        if (grupo.anterior && grupo.anterior.formId === form.getId()) {
          ligarDificuldade_(form, grupo.anterior.itemId, form.getItemById(criada.pagina).asPageBreakItem());
        }
        grupo.anterior = { formId: form.getId(), itemId: criada.dificuldade };
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
      grupo.anterior = null;
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
  if (!estado || estado.versao !== 4) {
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
  const novo = function (titulo) {
    return { titulo: titulo, questoes: [], proxima: 0, formIds: [], inicioParte: 0, anterior: null };
  };
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
    'avalie o contexto usado para gerar a questão, dê o parecer sobre a questão e diga se concorda ' +
    'com a nossa classificação de dificuldade.\n\n' +
    'Sua tarefa é apenas avaliar: não é preciso reescrever nem corrigir as questões. ' +
    'Quando marcar "Rejeitado" ou "Aprovado com ressalvas", escreva o motivo no campo logo abaixo.' +
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

/**
 * Cria a página da questão e a página condicional de discordância da dificuldade.
 * Devolve {pagina, dificuldade} (ids) ou null, sem deixar itens soltos, se o formulário atingiu o limite.
 * "Concordo" leva à próxima questão (ligado quando ela é criada; na última, envia o formulário);
 * "Discordo" abre a página em que o especialista dá a classificação dele e marca os motivos.
 */
function adicionarQuestao_(form, q, n, total) {
  const criados = [];
  const add = function (item) { criados.push(item); return item; };
  const c = q.codigo;
  try {
    const pagina = add(form.addPageBreakItem())
      .setTitle(c + ' · Questão ' + n + ' de ' + total)
      .setHelpText('Tópico: ' + q.topico + '\nSubtópico: ' + q.subtopico);
    add(form.addSectionHeaderItem()).setTitle('Enunciado').setHelpText(q.pergunta);
    add(form.addSectionHeaderItem()).setTitle('Resposta correta').setHelpText(q.resposta);
    if (q.pontos_essenciais && q.pontos_essenciais.length) {
      add(form.addSectionHeaderItem()).setTitle('Critério de correção (o que uma resposta precisa conter)')
        .setHelpText(q.pontos_essenciais.map(function (p) { return '• ' + p; }).join('\n'));
    }
    if (q.explicacao) {
      add(form.addSectionHeaderItem()).setTitle('Justificativa da resposta').setHelpText(q.explicacao);
    }
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
      .setHelpText('Obrigatório se marcou "Rejeitado" ou "Aprovado com ressalvas".');
    const dif = add(form.addMultipleChoiceItem());
    dif.setTitle(c + ' · Nossa classificação de dificuldade: ' + q.dificuldade.toUpperCase() + '. Você concorda?')
      .setHelpText('Considere um profissional que atua em operação de FPSOs.')
      .setChoices([dif.createChoice(CONCORDO, FormApp.PageNavigationType.SUBMIT),
                   dif.createChoice(DISCORDO, FormApp.PageNavigationType.CONTINUE)])
      .setRequired(true);
    add(form.addPageBreakItem())
      .setTitle(c + ' · Sua classificação de dificuldade')
      .setHelpText('Você discordou da nossa classificação (' + q.dificuldade + ').');
    add(form.addMultipleChoiceItem())
      .setTitle(c + ' · Qual classificação você daria?')
      .setChoiceValues(NIVEIS.filter(function (x) { return x !== q.dificuldade; }))
      .setRequired(true);
    add(form.addCheckboxItem())
      .setTitle(c + ' · Por que essa classificação?')
      .setHelpText('Marque todas as opções que se aplicam. Use "Outro" se nenhuma descrever o motivo.')
      .setChoiceValues(MOTIVOS_DIFICULDADE)
      .showOtherOption(true)
      .setRequired(true);
    return { pagina: pagina.getId(), dificuldade: dif.getId() };
  } catch (e) {
    criados.reverse().forEach(function (item) {
      try { form.deleteItem(item); } catch (ignorado) { /* item já inexistente */ }
    });
    if (/m[áa]ximo de itens|maximum number of items|too many items/i.test(String(e && e.message || e))) {
      return null;
    }
    throw e;
  }
}

/** "Concordo" na questão anterior passa a levar à página da questão recém-criada. */
function ligarDificuldade_(form, itemId, proximaPagina) {
  const mc = form.getItemById(itemId).asMultipleChoiceItem();
  mc.setChoices([mc.createChoice(CONCORDO, proximaPagina),
                 mc.createChoice(DISCORDO, FormApp.PageNavigationType.CONTINUE)]);
}
