@echo off

:main

  :: Store current directory and change to directory of this batch file
  pushd "%~dp0"

  :: Go two directories up, to the root of the directory
  cd ..\..

  :: Global environment variables, that we assume everybody has
  set HISPARC_ROOT=%CD%

  :: sets %HISPARC_DRIVE%
  :: set HISPARC_DRIVE=Z

  :: Append semicolon to %PYTHONPATH% if and only if it already exists
  if not "%PYTHONPATH%"=="" set PYTHONPATH=%PYTHONPATH%;

  :: ADL: Change all HISPARC_DRIVE references to the current working dir
  ::      or to the path stored in the Windows registry
  set PYTHONPATH=%PYTHONPATH%%HISPARC_ROOT%\user\pythonshared

  :: Create virtual drive
  :: subst %HISPARC_DRIVE%: "%HISPARC_ROOT%" > NUL

  :: The python-windows bindings assume that the files in the
  :: python\Lib\site-packages\pywin32_system32 directory were copied to
  :: system32. We don not want that because that would be mean that whenever
  :: this changes (for example, possibly with a python version upgrade), the
  :: admin-updater would need to be run.
  ::
  :: Instead, we add the directory containing these DLL files to the PATH before
  :: starting any application. because this startup script calls the start
  :: scripts, everything we run inherits this environment.
  :: set path=%path%;%HISPARC_DRIVE%:\user\python\Lib\site-packages\pywin32_system32

  :: DF: UNFORTUNATELY, this does not work anymore. I have copied around some
  ::     dll's and manifests and we now add the python directory to the path.
  set path=%path%;%HISPARC_ROOT%\user\python

  :: Go back to original current directory
  popd
