@echo off

if not "%USERNAME%" == "hisparc" exit

@call "%~dp0\..\..\user\startstop\runmanually.bat" \user\startstop StartUserMode.py
@pause
