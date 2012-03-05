@echo off

:: set up environment variables
call "%~dp0"/user/startstop/setenv.bat

:: change to HiSPARC root path
cd /d %HISPARC_ROOT%

:: start command interface
cmd /k "title hisparc_cmd"
