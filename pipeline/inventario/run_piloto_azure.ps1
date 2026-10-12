param(
    [string]$Python = "python",
    [string]$Manifest = "dataset/domain_corpora/manifest.json",
    [string]$Output = "pipeline/inventario/saida_piloto_kpi_azure",
    [switch]$Plan,
    [switch]$CheckApi,
    [switch]$AllowSampleCorpus,
    [ValidateSet('assuntos', 'varredura', 'selecao', 'extracao', 'consolidacao', 'fichas')]
    [string]$PararApos = "fichas"
)
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "../.."))
$invArgs = @('-u', 'pipeline/inventario/run_inventario.py', '--corpus-manifest', $Manifest,
    '--topicos', 'KPI',
    '--llm-provider', 'azure', '--llm-model', 'gpt-5-4-petrobras', '--effort', 'medium',
    '--embedder', 'embedding-3-large-global', '--reranker', 'none',
    '--workers', '2', '--max-chamadas', '400', '--output', $Output, '--parar-apos', $PararApos)
if ($Plan) { $invArgs += '--plan' }
if ($CheckApi) { $invArgs += '--check-api' }
if ($AllowSampleCorpus) { $invArgs += '--allow-sample-corpus' }
& $Python @invArgs
if ($LASTEXITCODE -ne 0) { throw "O piloto falhou (exit=$LASTEXITCODE). Consulte execucao.log e falhas_extracao.json." }
