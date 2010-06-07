@echo off

:main

  :: store current directory and change to directory of this batch file
  pushd "%~dp0"

  :: go two directories up, to the root of the directory
  cd ..\..

  :: global environment variables, that we assume everybody has
  set HISPARC_ROOT=%CD%

  :: sets %HISPARC_DRIVE%.
  call persistent\configuration\startup_settings.bat

  :: append semicolon to %PYTHONPATH% if and only if it already exists
  if not "%PYTHONPATH%"=="" set PYTHONPATH=%PYTHONPATH%;

  set PYTHONPATH=%PYTHONPATH%%HISPARC_DRIVE%:\user\pythonshared

  subst %HISPARC_DRIVE%: "%HISPARC_ROOT%" > NUL

  :: the python-windows bindings assume that the files in the python\Lib\site-packages\pywin32_system32
  :: directory were copied to system32. we don't want that because that would be mean that whenever this
  :: changes (for example, possibly with a python version upgrade), the admin-updater would need to be run.
  ::
  :: instead, we add the directory containing these DLL files to the PATH before starting any application.
  :: because this startup script calls the start scripts, everything we run inherits this environment
  :: set path=%path%;%HISPARC_DRIVE%:\user\python\Lib\site-packages\pywin32_system32
  :: DF: UNFORTUNATELY, this doesn't work anymore.  I've copied around
  :: some dll's and manifests and we now add the python directory to the
  :: path.
  set path=%path%;%HISPARC_DRIVE%:\user\python

  :: go back to original current directory
  popd
