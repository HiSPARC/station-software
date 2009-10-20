@echo off

:: set up environment variables and create virtual drive
call "%~dps0"\user\startstop\setenv.bat

:: change to virtual drive
%HISPARC_DRIVE%:

:: start command interface
cmd /k "title hisparc_cmd"