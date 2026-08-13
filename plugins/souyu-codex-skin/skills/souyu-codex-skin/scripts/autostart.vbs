' Codex Lite Skin - keeper watcher autostart (hidden window)
Set sh = CreateObject("WScript.Shell")
sh.Run "powershell -NoProfile -ExecutionPolicy Bypass -File ""C:\Users\wubin\.codex\skills\souyu-codex-skin\scripts\watch.ps1"" -Port 9335", 0, False
