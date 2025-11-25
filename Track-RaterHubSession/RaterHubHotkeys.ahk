#Requires AutoHotkey v2.0+

; ---------------------------------------------------------------
; Configuration
; ---------------------------------------------------------------
signalFolder := "C:\RaterHubTracker"
signalFile   := signalFolder "\signals.txt"

if !DirExist(signalFolder) {
    DirCreate(signalFolder)
}

LogRaterHubSignal(cmd) {
    global signalFile
    timestamp := FormatTime(A_Now, "yyyyMMddTHHmmss")
    line := cmd " " timestamp "`n"
    FileAppend(line, signalFile, "UTF-8")
}

; ---------------------------------------------------------------
; Hotkeys (only when Edge is active)
; ---------------------------------------------------------------
#HotIf WinActive("ahk_exe msedge.exe")

; Ctrl+Q → NEXT
^q::{
    LogRaterHubSignal("NEXT")
}

; Ctrl+Alt+Q → PAUSE / RESUME toggle
^!q::{
    LogRaterHubSignal("PAUSE")
}

; Ctrl+Shift+Q → END session
^+q::{
    LogRaterHubSignal("EXIT")
}

#HotIf
