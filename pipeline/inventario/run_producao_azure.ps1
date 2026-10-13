param(
    [string]$Python = "python",
    [string]$Manifest = "dataset/domain_corpora/manifest.json",
    [string]$Output = "pipeline/inventario/saida_producao_v4_notas",
    [string]$Reuse = "pipeline/inventario/saida_producao_v3_correcao_azure",
    [string[]]$Subtopicos = @(),
    [int]$Workers = 8,
    [int]$LimiteAssuntos = 0,
    [switch]$Plan,
    [switch]$CheckApi,
    [switch]$AllowSampleCorpus,
    [ValidateSet('assuntos', 'varredura', 'selecao', 'fatos', 'conceitos', 'notas', 'combinacoes', 'documentos')]
    [string]$PararApos = "documentos"
)
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "../.."))
# Filtro ASCII para compatibilidade com Windows PowerShell 5.1.
$invArgs = @('-u', 'pipeline/inventario/run_inventario.py', '--corpus-manifest', $Manifest,
    '--topicos', 'Processo (Medi', '--llm-provider', 'azure', '--llm-model', 'gpt-5-4-petrobras',
    '--effort', 'medium', '--embedder', 'embedding-3-large-global', '--reranker', 'none',
    '--workers', "$Workers", '--max-chamadas', '30000', '--output', $Output, '--parar-apos', $PararApos)
if ($Reuse -and (Test-Path $Reuse)) { $invArgs += @('--reaproveitar-de', $Reuse) }
if ($Subtopicos.Count -gt 0) { $invArgs += '--subtopicos'; $invArgs += $Subtopicos }
if ($LimiteAssuntos -gt 0) { $invArgs += @('--limite-assuntos', "$LimiteAssuntos") }
if ($Plan) { $invArgs += '--plan' }
if ($CheckApi) { $invArgs += '--check-api' }
if ($AllowSampleCorpus) { $invArgs += '--allow-sample-corpus' }
& $Python @invArgs
if ($LASTEXITCODE -ne 0) { throw "Execução interrompida (exit=$LASTEXITCODE). Veja execucao.log e ocorrencias.jsonl." }
