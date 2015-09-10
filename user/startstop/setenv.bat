@echo off

::
:: setenv.bat ---
:: Sets HISPARC_ROOT, home of HiSPARC.
::
:: Modified Feb 2012; No HISPARC_DRIVE anymore!! (RH)
::

:main

  :: store current directory and change to directory of this batch file
  pushd "%~dp0"

  :: go two directories up, to the root of HiSPARC
  cd ..\..
  set HISPARC_ROOT=%CD%
  :: echo setenv.bat: HISPARC_ROOT=%HISPARC_ROOT%

  :: append semicolon to %PYTHONPATH% if and only if it already exists
  if not "%PYTHONPATH%"=="" set PYTHONPATH=;%PYTHONPATH%
  set PYTHONPATH=%HISPARC_ROOT%\user\pythonshared%PYTHONPATH%
  :: echo setenv.bat: PYTHONPATH=%PYTHONPATH%

  :: put HiSPARC's python in front of path
  set path=%HISPARC_ROOT%\user\python;%path%
  :: echo setenv.bat: path=%path%

  :: go back to original current directory
  popd
