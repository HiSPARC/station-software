@echo off

::
:: runmanually.bat ---
::
:: Modified Feb 2012; No virtual drive (HISPARC_DRIVE) anymore!! (RH)
::
:: Batch file to help running applications in the context of the HiSPARC
:: system. Sets the environment variables and launches the specified COMMAND in
:: the specified PATH. If COMMAND ends with ".py", the python interpreter
:: (as part of the HiSPARC distribution) is automatically used.
:: Otherwise, COMMAND is simply executed as if it were typed on the command line.
::
:: Note: the name of this file is slightly incorrect: it has nothing to do
:: with whether a program is run manually or automatically - it just runs the
:: program.
::
:: invoke as:
::   @call "%~dp0..\startstop\runmanually.bat" NAME PATH COMMAND [args]
::
:: example:
::   @call "%~dp0..\startstop\runmanually.bat" "HiSPARC Monitor" \user\hsmonitor hsmonitor.py
::
:: set the NAME to 0 to execute the command in the same window
:: example:
::   @call "%~dp0..\startstop\runmanually.bat" 0 \user\diagnostictool gui.py
::

:main

  set HISPARC_RUNMANUAL_PATH=%~1
  set HISPARC_RUNMANUAL_CMD=%~2
  set HISPARC_RUNMANUAL_NAME=%~3

  :: call setenv to set the environment variables and path
  call "%~dp0setenv.bat"
  
  :: go to application directory
  pushd %HISPARC_ROOT%%HISPARC_RUNMANUAL_PATH%

  if "%HISPARC_RUNMANUAL_CMD:~-3%"==".py" (
    call :python %*
  ) else (
    call :exe %*
  )
  
  :: actually execute application
  :: Start programs in a new process to allow them to be terminated
  if "%HISPARC_RUNMANUAL_NAME%" == "0" (
    %HISPARC_RUNMANUAL_DO%
  ) else (
    start %HISPARC_RUNMANUAL_NAME% %HISPARC_RUNMANUAL_DO%
  )

  :: switch back to old drive
  popd
  goto :EOF


:python

  shift /1
  shift /1
  shift /1
  set HISPARC_RUNMANUAL_DO=python.exe %HISPARC_RUNMANUAL_CMD% %1 %2 %3 %4 %5 %6 %7 %8 %9 
  goto :EOF


:exe

  shift /1
  shift /1
  shift /1
  set HISPARC_RUNMANUAL_DO=%HISPARC_RUNMANUAL_CMD% %1 %2 %3 %4 %5 %6 %7 %8 %9
  goto :EOF
