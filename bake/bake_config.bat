@echo off

:: HSBAKE: bake_config.bat
:: sets up all necessary configuration environment variables

:: include user-specified settings
call bake_settings.bat

:: HSBAKE_BAKE_DIR
set HSBAKE_BAKE_DIR_=%~dps0
:: remove trailing slash
set HSBAKE_BAKE_DIR=%HSBAKE_BAKE_DIR_:~0,-1%
set HSBAKE_BAKE_DIR_=

:: HSBAKE_HOME_DIR
pushd %HSBAKE_BAKE_DIR%\..
set HSBAKE_HOME_DIR=%CD%
popd


set HSBAKE_USER_DIR=%HSBAKE_HOME_DIR%\user
set HSBAKE_ADMIN_DIR=%HSBAKE_HOME_DIR%\admin
set HSBAKE_PERSISTENT_DIR=%HSBAKE_HOME_DIR%\persistent
set HSBAKE_BACKUP_DIR=%HSBAKE_BAKE_DIR%\backup
