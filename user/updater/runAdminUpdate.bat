@call "%~dp0\..\..\user\startstop\runmanually.bat" 0 \user\startstop StopUserMode.py
@call "%~dp0\..\..\user\startstop\runmanually.bat" 0 \user\startstop StopAdminMode.py

@call "%1" 

@call "%~dp0\..\..\user\startstop\runmanually.bat" 0 \user\startstop StartUserMode.py
@call "%~dp0\..\..\user\startstop\runmanually.bat" 0 \user\startstop StartAdminMode.py
