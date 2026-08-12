param([int]$Port = 9335)

$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$StateRoot = Join-Path $env:LOCALAPPDATA 'CodexLiteSkin'
New-Item -ItemType Directory -Force -Path $StateRoot | Out-Null
$StatePath = Join-Path $StateRoot 'state.json'

function Test-Cdp([int]$P) {
  foreach ($lb in @('127.0.0.1', '[::1]')) {
    try {
      $t = Invoke-RestMethod "http://$($lb):$P/json/list" -TimeoutSec 1
      if ($t | Where-Object { $_.type -eq 'page' -and $_.url -like 'app://*' }) { return $true }
    } catch {}
  }
  return $false
}

# 1. Make sure Codex runs with the debug port (restarts it once if needed).
if (-not (Test-Cdp $Port)) {
  Write-Host 'Restarting Codex with the skin port...'
  Get-Process ChatGPT -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | ForEach-Object { [void]$_.CloseMainWindow() }
  Start-Sleep -Seconds 2
  Get-Process ChatGPT -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Milliseconds 900
  Get-Process ChatGPT -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  $pkg = Get-AppxPackage OpenAI.Codex | Sort-Object Version -Descending | Select-Object -First 1
  if (-not $pkg) { throw 'OpenAI.Codex package not found.' }
  $exe = Join-Path $pkg.InstallLocation 'app\ChatGPT.exe'
  Start-Process -FilePath $exe -ArgumentList "--remote-debugging-port=$Port"
  $deadline = (Get-Date).AddSeconds(45)
  while (-not (Test-Cdp $Port) -and (Get-Date) -lt $deadline) { Start-Sleep -Milliseconds 500 }
  if (-not (Test-Cdp $Port)) { throw "Codex did not expose CDP on port $Port." }
}

# 2. (Re)start the injector.
if (Test-Path -LiteralPath $StatePath) {
  try {
    $old = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
    if ($old.injectorPid) { Stop-Process -Id ([int]$old.injectorPid) -Force -ErrorAction SilentlyContinue }
  } catch {}
}
$node = (Get-Command node).Source
$inj = Start-Process -FilePath $node -WindowStyle Hidden -PassThru -ArgumentList @(
  "`"$(Join-Path $Root 'inject.mjs')`"", '--watch', '--port', "$Port"
) -RedirectStandardOutput (Join-Path $StateRoot 'injector.log') -RedirectStandardError (Join-Path $StateRoot 'injector-error.log')
@{ port = $Port; injectorPid = $inj.Id; startedAt = (Get-Date).ToString('o'); root = $Root } |
  ConvertTo-Json | Set-Content -LiteralPath $StatePath -Encoding utf8

# 3. Ensure the keeper watcher runs (re-injects after normal Codex restarts).
$already = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
  Where-Object { $_.CommandLine -like '*codex-lite-skin*watch.ps1*' }
if (-not $already) {
  Start-Process powershell -WindowStyle Hidden -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $Root 'watch.ps1'), '-Port', "$Port"
  )
}

Start-Sleep -Seconds 2
Write-Host "Codex Lite Skin active on port $Port (injector $($inj.Id))."
