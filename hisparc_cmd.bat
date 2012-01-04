@echo off

:: set up environment variables and create virtual drive
call "%~dps0"\user\startstop\setenv.bat

:: change to HiSPARC root path
%HISPARC_ROOT%:

:: start command interface
cmd /k "title hisparc_cmd"