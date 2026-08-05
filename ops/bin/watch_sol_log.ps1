$Host.UI.RawUI.WindowTitle = 'Sol activity log (live)'
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content -LiteralPath 'C:\Users\81905\Desktop\shadow-atelier\ops\codex_activity.log' -Tail 40 -Wait -Encoding UTF8
