@echo off

if not "%USERNAME%" == "hisparc" exit

@reg add "HKCU\Control Panel\Desktop" /v ScreenSaveActive /d 0 /f

@call "%~dp0\..\..\user\startstop\runmanually.bat" \user\startstop StartUserMode.py
@pause
