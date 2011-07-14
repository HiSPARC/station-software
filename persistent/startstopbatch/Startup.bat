@ECHO OFF
IF NOT "%USERNAME%" == "hisparc" EXIT

@call "%~dp0\..\..\user\startstop\runmanually.bat" \user\startstop StartUserMode.py
@pause

