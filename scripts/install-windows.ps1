<#
.SYNOPSIS
  Installs the video-editing workspace toolchain on Windows (winget).
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

# --- faster-whisper ---
Say 'faster-whisper (Python)'
if (Has python) {
  python -c "import faster_whisper" *> $null
  if ($LASTEXITCODE -eq 0) { Ok "faster-whisper $(python -c 'import faster_whisper; print(faster_whisper.__version__)')" }
  elseif (Confirm-Step 'Install faster-whisper with pip?') {
    python -m pip install --upgrade faster-whisper
    if ($LASTEXITCODE -ne 0) { Warn 'pip install failed' }
  } else { Warn 'Skipped faster-whisper' }
} else { Warn 'python missing, cannot install faster-whisper (open a new terminal after installing Python)' }

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

# --- HyperFrames doctor ---
Say 'HyperFrames doctor'
if (Has npx) {
  npx --yes hyperframes doctor
  if ($LASTEXITCODE -ne 0) { Warn 'hyperframes doctor reported problems' }
} else { Warn 'npx missing, skipping doctor' }

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
if (Has python) {
  $fw = python -c "import faster_whisper; print(faster_whisper.__version__)" 2>$null
  if ($LASTEXITCODE -ne 0) { $fw = 'MISSING' }
  '  {0,-15} {1}' -f 'faster-whisper', $fw
}
Write-Host "`nDone. Open a new terminal if a tool still shows MISSING right after install."
