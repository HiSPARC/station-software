@echo off

:: get configuration settings
call bake_config.bat

if "%HSBAKE_PYTHON_SOURCE_DIR%"=="" goto noconf

if "%~1"=="checkonly" goto check

:: clean up backup directory, if any
rem mkdir %HSBAKE_BACKUP_DIR%\python 2>1 NUL
rem del /s /q %HSBAKE_BACKUP_DIR%\python 2>1 NUL
echo cleaning up old backup directory (%HSBAKE_BACKUP_DIR%), if any...
mkdir %HSBAKE_BACKUP_DIR% 2>1 NUL
rmdir /s /q %HSBAKE_BACKUP_DIR%\python 2>1 NUL


:: rename current python dir to backup directory
echo moving %HSBAKE_USER_DIR%\python to %HSBAKE_BACKUP_DIR%...
move %HSBAKE_USER_DIR%\python %HSBAKE_BACKUP_DIR%
echo copying %HSBAKE_PYTHON_SOURCE_DIR%\* to %HSBAKE_USER_DIR%\python, please hold...
xcopy /e /h /i /q %HSBAKE_PYTHON_SOURCE_DIR%\*.* %HSBAKE_USER_DIR%\python

:check

echo checking python installation..
:: check for executable
%HSBAKE_USER_DIR%\python\python.exe --help > NUL
IF ERRORLEVEL 1 goto buisfault

:: run pytest.py
%HSBAKE_USER_DIR%\python\python.exe %HSBAKE_BAKE_DIR%\pytest.py
IF ERRORLEVEL 1 goto buisfault

goto success

:buisfault
echo One or more checks failed.. Please check or rerun the import process
goto eof

:success
echo Python import succeeded.
goto :eof

:noconf
echo  make sure HSBAKE_PYTHON_SOURCE_DIR is set in bake_settings.bat
goto eof


:eof