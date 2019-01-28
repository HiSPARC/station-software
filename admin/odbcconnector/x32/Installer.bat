@ECHO OFF

pushd "%~dp0"
call Install.bat
set retCode=%ERRORLEVEL%
popd

IF %retCode% NEQ 0 ping 1.1.1.1 -n 1 -w 5000 > nul

EXIT /B %retCode%
