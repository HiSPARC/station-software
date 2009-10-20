@call "%~dp0\..\..\user\startstop\runmanually.bat" \user\startstop StopUserMode.py

@call "%1" 

@call "%~dp0\..\..\user\startstop\runmanually.bat" \user\startstop StartUserMode.py