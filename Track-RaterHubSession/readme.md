# RaterHub Tracker – Quick Start

## What this tool does
Tracks RaterHub sessions using PowerShell 7 + AutoHotkey v2:
- Per-question timing (pauses excluded)
- Session HTML dashboards
- End-of-day daily reports

## Requirements
- **PowerShell 7**
- **AutoHotkey v2**

## Hotkeys (active only in Edge)
- **Ctrl+Q** → Next question  
- **Ctrl+Alt+Q** → Pause/Resume  
- **Ctrl+Shift+Q** → End session  
- *(Optional)* **Ctrl+Win+D** → Generate daily report  

## Start a live session
```powershell
pwsh C:\Scripts\RaterHubTracker.ps1 -LaunchEdgeIfNeeded
```

## End-of-day daily report
```powershell
pwsh C:\Scripts\New-RaterHubDailyReport.ps1
```

## Output files
Located in: `Documents\RaterHubTracker\`