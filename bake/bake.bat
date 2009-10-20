@echo off

:: get configuration settings
call bake_config.bat

call "%~dp0..\user\python\python.exe" "bakescripts\bake.py"

pause