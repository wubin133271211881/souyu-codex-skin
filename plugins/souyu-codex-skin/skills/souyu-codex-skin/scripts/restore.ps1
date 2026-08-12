param([int]$Port = 9335)

$ErrorActionPreference = 'Continue'
$Root = $PSScriptRoot
$StateRoot = Join-Path $env:LOCALAPPDATA 'CodexLiteSkin'
$StatePath = Join-Path $StateRoot 'state.json'

# Stop the keeper watcher (matches the mutex name used by watch.ps1).
$watcher = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
  Where-Object { $_.CommandLine -like '*codex-lite-skin*watch.ps1*' }
foreach ($w in $watcher) { Stop-Process -Id $w.ProcessId -Force -ErrorAction SilentlyContinue }

# Stop the injector.
if (Test-Path -LiteralPath $StatePath) {
  try {
    $state = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
    if ($state.injectorPid) { Stop-Process -Id ([int]$state.injectorPid) -Force -ErrorAction SilentlyContinue }
  } catch {}
}

# Remove the injected style from the running app (if the debug port is up).
$node = (Get-Command node).Source
& $node (Join-Path $Root 'inject.mjs') --remove --port $Port 2>$null

Write-Host 'Codex Lite Skin removed. Codex will look default again (colors from your config still apply).'
