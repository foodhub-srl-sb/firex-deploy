<#
.SYNOPSIS
  Installs the Food Hub video studio toolchain on Windows (winget): Node 22+, FFmpeg,
  Poppler, Python packages (requirements.txt), Claude Code + HyperFrames, Chrome for
  rendering, RobustVideoMatting models.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1 [-Yes]
#>
param([switch]$Yes)

$ErrorActionPreference = 'Stop'

function Say($m)  { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Ok($m)   { Write-Host "  ok  $m" -ForegroundColor Green }
function Warn($m) { Write-Host "  !!  $m" -ForegroundColor Yellow }
function Has($c)  { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

function Confirm-Step($q) {
  if ($Yes) { return $true }
  $r = Read-Host "  $q [y/N]"
  return ($r -match '^[Yy]$')
}

# Reload PATH so freshly installed tools are visible in this session.
function Update-Path {
  $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
              [Environment]::GetEnvironmentVariable('Path', 'User')
}

function Winget-Install($id, $label) {
  if (Confirm-Step "Install $label with 'winget install $id'?") {
    winget install --id $id -e --accept-source-agreements --accept-package-agreements
    Update-Path
  } else { Warn "Skipped $label" }
}

function Node-Major {
  try { [int]((node -p "process.versions.node.split('.')[0]") 2>$null) } catch { 0 }
}

if (-not (Has winget)) {
  Write-Error "winget not found. Install 'App Installer' from the Microsoft Store and retry."
  exit 1
}

# --- Node.js 22+ ---
Say 'Node.js (>= 22)'
if ((Has node) -and ((Node-Major) -ge 22)) { Ok "node $(node --version)" }
else {
  if (Has node) { Warn "node $(node --version) is older than 22" }
  Winget-Install 'OpenJS.NodeJS.LTS' 'Node.js LTS'
  if ((Has node) -and ((Node-Major) -lt 22)) { Warn 'node is still < 22: winget upgrade OpenJS.NodeJS.LTS' }
}

# --- FFmpeg ---
Say 'FFmpeg'
if ((Has ffmpeg) -and (Has ffprobe)) { Ok ((ffmpeg -version | Select-Object -First 1)) }
else { Winget-Install 'Gyan.FFmpeg' 'FFmpeg' }

# --- Python ---
Say 'Python 3'
# 'python' may be the Microsoft Store alias stub; test that it actually runs.
$pyOk = $false
if (Has python) { try { python --version *> $null; $pyOk = ($LASTEXITCODE -eq 0) } catch {} }
if ($pyOk) { Ok (python --version) }
else { Winget-Install 'Python.Python.3.13' 'Python 3.13' }

# --- Poppler (PDF tools: pdftotext, pdfimages, pdftocairo) ---
Say 'Poppler (PDF tools)'
if ((Has pdftotext) -and (Has pdfimages) -and (Has pdftocairo)) { Ok 'pdftotext present' }
else {
  Winget-Install 'oschwartz10612.Poppler' 'Poppler'
  if (-not (Has pdftotext)) { Warn 'Poppler installed but not on PATH yet: open a new terminal (or add its Library\bin folder to PATH)' }
}

# --- Python packages (requirements.txt) ---
Say 'Python packages (faster-whisper, numpy, scipy, pillow, onnxruntime)'
$Root = Split-Path -Parent $PSScriptRoot
if (Has python) {
  python -c "import faster_whisper, numpy, scipy, PIL, onnxruntime" *> $null
  if ($LASTEXITCODE -eq 0) { Ok 'all Python packages present' }
  elseif (Confirm-Step 'Install the Python packages from requirements.txt?') {
    python -m pip install --upgrade -r (Join-Path $Root 'requirements.txt')
    if ($LASTEXITCODE -ne 0) { Warn 'pip install failed' }
  } else { Warn 'Skipped Python packages' }

  # Faster person cutouts (RVM) on the graphics card
  python -c "import onnxruntime as o; import sys; sys.exit(0 if ({'CUDAExecutionProvider','DmlExecutionProvider'} & set(o.get_available_providers())) else 1)" *> $null
  if ($LASTEXITCODE -ne 0) {
    if (Has nvidia-smi) { $gpuPkg = 'onnxruntime-gpu'; $gpuLabel = 'NVIDIA GPU found' }
    else { $gpuPkg = 'onnxruntime-directml'; $gpuLabel = 'No NVIDIA GPU: DirectML works with most graphics cards' }
    if (Confirm-Step "$gpuLabel. Switch to $gpuPkg for faster person cutouts (RVM)?") {
      python -m pip uninstall -y onnxruntime *> $null
      python -m pip install --upgrade $gpuPkg
      if ($LASTEXITCODE -ne 0) { Warn "$gpuPkg install failed: reinstall the CPU version with 'python -m pip install onnxruntime'" }
    }
  }
} else { Warn 'python missing, cannot install Python packages (open a new terminal after installing Python)' }

# --- Claude Code + HyperFrames plugin ---
Say 'Claude Code + HyperFrames plugin'
if (Has claude) {
  Ok "claude $(claude --version)"
  if (Confirm-Step 'Add HyperFrames marketplace and install the plugin?') {
    claude plugin marketplace add heygen-com/hyperframes
    if ($LASTEXITCODE -ne 0) { Warn 'marketplace add failed (maybe already added)' }
    claude plugin install hyperframes@hyperframes
    if ($LASTEXITCODE -ne 0) { Warn 'plugin install failed (maybe already installed)' }
  }
} else {
  Warn 'Claude Code not found. Install it with:'
  Write-Host '      irm https://claude.ai/install.ps1 | iex'
  Write-Host '    then re-run this script to add the HyperFrames plugin.'
}

# --- HyperFrames: Chrome for rendering + doctor ---
Say 'HyperFrames (Chrome for rendering + doctor)'
if (Has npx) {
  npx --yes hyperframes browser ensure
  if ($LASTEXITCODE -ne 0) { Warn 'could not prepare Chrome for rendering' }
  npx --yes hyperframes doctor
  if ($LASTEXITCODE -ne 0) { Warn 'hyperframes doctor reported problems' }
} else { Warn 'npx missing, skipping HyperFrames setup' }

# --- RobustVideoMatting models (person cutouts) ---
Say 'RobustVideoMatting models (~120 MB, once)'
if (Has python) {
  python -c "import onnxruntime" *> $null
  if (($LASTEXITCODE -eq 0) -and (Confirm-Step 'Download the RVM models now?')) {
    python (Join-Path $Root 'scripts\rvm-matte.py') --prepare
    if ($LASTEXITCODE -ne 0) { Warn 'model download failed (it will retry on first use)' }
  }
}

# --- OpenRouter key (optional, for AI images and video from this PC) ---
Say 'OpenRouter (optional)'
if ($env:OPENROUTER_API_KEY) { Ok 'OPENROUTER_API_KEY is set' }
else {
  Write-Host '  AI generation already works through the GitHub Action (repository secret).'
  Write-Host '  To generate directly from this PC, run once (never put the key in a file in the repo):'
  Write-Host '      setx OPENROUTER_API_KEY "sk-or-..."'
}

# --- Summary ---
Say 'Installed versions'
function V($name, [scriptblock]$cmd) {
  if (Has $name) {
    $out = try { (& $cmd 2>$null | Select-Object -First 1) } catch { '?' }
    '  {0,-15} {1}' -f $name, $out
  } else { '  {0,-15} {1}' -f $name, 'MISSING' }
}
V node    { node --version }
V npm     { npm --version }
V ffmpeg  { (ffmpeg -version)[0] }
V ffprobe { (ffprobe -version)[0] }
V python  { python --version }
V claude  { claude --version }
V pdftotext { (pdftotext -v 2>&1)[0] }
if (Has python) {
  foreach ($mod in 'faster_whisper','numpy','scipy','PIL','onnxruntime') {
    $ver = python -c "import $mod; print(getattr($mod, '__version__', 'ok'))" 2>$null
    if ($LASTEXITCODE -ne 0) { $ver = 'MISSING' }
    '  {0,-15} {1}' -f $mod, $ver
  }
}
Write-Host "`nDone. Open a new terminal if a tool still shows MISSING right after install."
