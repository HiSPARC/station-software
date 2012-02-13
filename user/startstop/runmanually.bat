@echo off
:: Batch file to help running applications in the context of the HiSPARC
:: virtual drive. Sets the environment variables, creates the virtual drive
:: if it does not yet exists, and launches the specified COMMAND in
:: the specified PATH. If COMMAND ends with ".py", the python interpreter
:: is automatically used. Otherwise, COMMAND is simply executed as if it were
:: typed on the command line.
::
:: Note: the name of this file is slightly incorrect: it has nothing to do
:: with whether a program is run manually or automatically - it just runs the
:: program.
::
:: invoke as 
::
::   @call "%~dp0..\startstop\runmanually.bat" PATH COMMAND [args]
::
:: examples:
::
::   @call "%~dp0..\startstop\runmanually.bat" \user\hsmonitor hsmonitor.py


:main

  set HISPARC_RUNMANUAL_PATH=%~1
  set HISPARC_RUNMANUAL_CMD=%~2
  
  :: call setenv and create virtual drive
  call "%~dp0setenv.bat"
  
  :: go to HiSPARC root and application directory
  
  pushd %HISPARC_ROOT%%HISPARC_RUNMANUAL_PATH%

  if "%HISPARC_RUNMANUAL_CMD:~-3%"==".py" (
    call :python %*
  ) else (
    call :exe %*
  )
  
  :: actually execute application
  %HISPARC_RUNMANUAL_DO%
  
  :: if an error occured, wait for keypress, else close.
  :: DF: removed because it breaks nagios checks
  ::if errorlevel 1 pause

  :: switch back to old drive
  popd
  
  goto :EOF


:python

  shift /1
  shift /1

  set HISPARC_RUNMANUAL_DO=\user\python\python.exe %HISPARC_RUNMANUAL_CMD% %1 %2 %3 %4 %5 %6 %7 %8 %9 

goto :EOF


:exe

  shift /1
  shift /1
  
  set HISPARC_RUNMANUAL_DO=%HISPARC_RUNMANUAL_CMD% %1 %2 %3 %4 %5 %6 %7 %8 %9

goto :EOF

