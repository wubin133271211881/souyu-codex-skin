param([int]$Port = 9335)

$ErrorActionPreference = 'Continue'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

$created = $false
$mutex = New-Object System.Threading.Mutex($true, "Local\CodexLiteSkinWatcher-$Port", [ref]$created)
if (-not $created) { exit 0 }

function Test-Cdp([int]$P) {
  foreach ($lb in @('127.0.0.1', '[::1]')) {
    try {
      $t = Invoke-RestMethod "http://$($lb):$P/json/list" -TimeoutSec 1
      if ($t | Where-Object { $_.type -eq 'page' -and $_.url -like 'app://*' }) { return $true }
    } catch {}
  }
  return $false
}

while ($true) {
  $cdpUp = Test-Cdp $Port
  $mainProcs = @(Get-Process ChatGPT -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 })
  if (-not $cdpUp -and $mainProcs.Count -gt 0) {
    $oldEnough = @($mainProcs | Where-Object {
      try { ((Get-Date) - $_.StartTime).TotalSeconds -ge 15 } catch { $true }
    })
    if ($oldEnough.Count -gt 0) {
      & (Join-Path $Root 'start.ps1') -Port $Port | Out-Null
    }
  }
  Start-Sleep -Seconds 3
}
