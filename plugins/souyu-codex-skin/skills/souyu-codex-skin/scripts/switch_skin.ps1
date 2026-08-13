param(
  [string]$Name,
  [string]$Remove,
  [int]$Port = 9335
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Py = (Get-Command python).Source
$SwitchPy = Join-Path $PSScriptRoot 'switch_skin.py'
$env:PYTHONIOENCODING = 'utf-8'

if ($Remove) {
  & $Py $SwitchPy --delete $Remove
  if ($LASTEXITCODE -ne 0) { throw "switch_skin.py --delete failed (exit $LASTEXITCODE)" }
  Write-Host 'Restarting injector to refresh the skin list...'
  & (Join-Path $PSScriptRoot 'start.ps1') -Port $Port
  if ($LASTEXITCODE -ne 0) { throw "start.ps1 failed (exit $LASTEXITCODE)" }
  Write-Host "Skin removed: $Remove"
  exit 0
}

if (-not $Name) {
  Write-Host 'Available skins:'
  $skins = @(& $Py $SwitchPy --list)
  if ($skins.Count -eq 0) { throw 'No skins registered.' }
  $skins | ForEach-Object { Write-Host "  $_" }
  $Name = Read-Host 'Enter skin id'
  if (-not $Name) { throw 'No skin selected.' }
}

& $Py $SwitchPy --skin $Name
if ($LASTEXITCODE -ne 0) { throw "switch_skin.py failed (exit $LASTEXITCODE)" }

Write-Host 'Restarting injector with the new skin...'
& (Join-Path $PSScriptRoot 'start.ps1') -Port $Port
if ($LASTEXITCODE -ne 0) { throw "start.ps1 failed (exit $LASTEXITCODE)" }

Write-Host 'Verifying...'
& node (Join-Path $PSScriptRoot 'check.mjs') --port $Port
if ($LASTEXITCODE -ne 0) { throw "check.mjs failed (exit $LASTEXITCODE)" }

Write-Host "Skin switched. Restore with: powershell -File $PSScriptRoot\restore.ps1 -Port $Port"
