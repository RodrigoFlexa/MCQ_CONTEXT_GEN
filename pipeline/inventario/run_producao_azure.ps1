param(
    [string]$Python = "python",
    [string]$Manifest = "dataset/domain_corpora/manifest.json",
    [string]$Output = "pipeline/inventario/saida_producao_v3_correcao_azure",
    [string[]]$Subtopicos = @(),
    [switch]$Plan,
    [switch]$CheckApi,
    [switch]$AllowSampleCorpus,
    [ValidateSet('assuntos', 'varredura', 'selecao', 'extracao', 'revisao', 'consolidacao', 'fichas')]
    [string]$PararApos = "fichas"
)
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "../.."))
# Filtro ASCII para compatibilidade com Windows PowerShell 5.1.
$invArgs = @('-u', 'pipeline/inventario/run_inventario.py', '--corpus-manifest', $Manifest,
    '--topicos', 'Processo (Medi', '--llm-provider', 'azure', '--llm-model', 'gpt-5-4-petrobras',
    '--effort', 'medium', '--embedder', 'embedding-3-large-global', '--reranker', 'none',
    '--workers', '2', '--review-batch', '8', '--max-chamadas', '30000',
    '--output', $Output, '--parar-apos', $PararApos)
if ($Subtopicos.Count -gt 0) { $invArgs += '--subtopicos'; $invArgs += $Subtopicos }
if ($Plan) { $invArgs += '--plan' }
if ($CheckApi) { $invArgs += '--check-api' }
if ($AllowSampleCorpus) { $invArgs += '--allow-sample-corpus' }
& $Python @invArgs
if ($LASTEXITCODE -ne 0) { throw "O piloto falhou (exit=$LASTEXITCODE). Consulte o log e os pareceres." }
