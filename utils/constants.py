SYSTEM_COMMANDS = {
    "shutdown": "shutdown /s /t 30",
    "restart": "shutdown /r /t 30",
    "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0",
    "lock": "rundll32.exe user32.dll,LockWorkStation",
}

QUICK_PROGRAMS = {
    "discord": "discord",
    "spotify": "spotify",
    "firefox": "firefox",
    "chrome": "google chrome",
    "explorer": "explorer",
    "notepad": "notepad",
    "calculator": "calculator",
}