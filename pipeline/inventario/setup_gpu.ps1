# Prepara o ambiente GPU do inventário: cria venv_gpu, instala PyTorch com CUDA
# compatível com o driver, instala as dependências e valida bge-m3/reranker na GPU.
#
# Uso (PowerShell, em qualquer pasta):
#   powershell -ExecutionPolicy Bypass -File pipeline/inventario/setup_gpu.ps1
#   powershell -ExecutionPolicy Bypass -File pipeline/inventario/setup_gpu.ps1 -Python C:\Users\rodri\anaconda3\python.exe
param(
    [string]$Python = "python",
    [string]$Venv = "venv_gpu"
)
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..\.."))

function Run($exe, [string[]]$argv) {
    & $exe @argv
    if ($LASTEXITCODE -ne 0) { throw "Falhou: $exe $($argv -join ' ')" }
}

$smi = (& nvidia-smi 2>$null) -join "`n"
if (-not $smi) { throw "nvidia-smi não encontrado. Instale ou atualize o driver NVIDIA e rode de novo." }
$m = [regex]::Match($smi, "CUDA Version:\s*(\d+)\.(\d+)")
if (-not $m.Success) { throw "Não consegui ler a versão CUDA suportada pelo driver (nvidia-smi)." }
$cuda = [int]$m.Groups[1].Value * 10 + [int]$m.Groups[2].Value
if ($cuda -ge 130) { $tag = "cu130" }
elseif ($cuda -ge 126) { $tag = "cu126" }
elseif ($cuda -ge 124) { $tag = "cu124" }
elseif ($cuda -ge 121) { $tag = "cu121" }
else { $tag = "cu118" }
Write-Host "Driver NVIDIA suporta CUDA $($m.Groups[1].Value).$($m.Groups[2].Value) -> PyTorch $tag"

if (-not (Test-Path "$Venv\Scripts\python.exe")) {
    Write-Host "Criando ambiente $Venv com $Python"
    Run $Python @("-m", "venv", $Venv)
}
$py = (Resolve-Path "$Venv\Scripts\python.exe").Path
Run $py @("-m", "pip", "install", "--upgrade", "pip")
Run $py @("-m", "pip", "install", "--upgrade", "torch", "--index-url", "https://download.pytorch.org/whl/$tag")
Run $py @("-m", "pip", "install", "-r", "pipeline\inventario\requirements.txt")
Run $py @("pipeline\inventario\check_gpu.py")
Write-Host ""
Write-Host "Ambiente pronto. Use este Python para rodar o inventário:"
Write-Host "  $py"
