@call "%~dp0\..\..\user\startstop\runmanually.bat" 0 \user\startstop StopUserMode.py

@call "%1" 

@call "%~dp0\..\..\user\startstop\runmanually.bat" 0 \user\startstop StartUserMode.py
