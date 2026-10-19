param(
    [string]$Python = "",
    [ValidateSet("auto", "cuda", "cpu")][string]$Device = "auto",
    [int]$BatchSize = 64
)
$ErrorActionPreference = "Stop"
$documentRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
Push-Location -LiteralPath $documentRoot
try {
    if (-not $Python) {
        $documentGpuPython = Join-Path $documentRoot ".venv-documento-gpu/Scripts/python.exe"
        if (Test-Path -LiteralPath $documentGpuPython) { $Python = $documentGpuPython }
        else { $Python = (Get-Command python).Source }
    }
    $env:PYTHONUTF8 = "1"
    & $Python -u -m pipeline.qa_research.document.batch prepare --device $Device --batch-size $BatchSize
    if ($LASTEXITCODE -ne 0) { throw "Preparação interrompida. Os caches e pacotes concluídos foram preservados." }
    & $Python -m pipeline.qa_research.document.batch check --report pipeline/qa_research/pacotes/dez_areas_v1/PREPARACAO.md
    if ($LASTEXITCODE -ne 0) { throw "Falha de integridade do lote preparado." }
    Write-Host "O código acabou de rodar no terminal :)"
    Write-Host "Para enviar os pacotes prontos:"
    Write-Host 'git add -- pipeline/qa_research/configs/dez_areas_v1 pipeline/qa_research/pacotes/dez_areas_v1'
    Write-Host 'git commit -m "Preparacao local das dez areas FPSO"'
    Write-Host 'git push origin codex/qa-evidencias-verificadas'
} finally { Pop-Location }
