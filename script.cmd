
@echo off

:: to delete the backdoor registry entry
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor

:: to play wave file in windows
powershell -c (New-Object Media.SoundPlayer 'c:\PathTo\YourSound.wav').PlaySync();

:: shutdown

:: reboot

