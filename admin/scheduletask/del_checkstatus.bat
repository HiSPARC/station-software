::::::::::::::::::::::::::::::::::::::::::::
:: Automatically check & get admin rights V2
::::::::::::::::::::::::::::::::::::::::::::
@echo off
CLS
::::::::::::::::::::::
:: Running Admin shell
::::::::::::::::::::::

:init
setlocal DisableDelayedExpansion
set "batchPath=%~0"
for %%k in (%0) do set batchName=%%~nk
set "vbsGetPrivileges=%temp%\OEgetPriv_%batchName%.vbs"
setlocal EnableDelayedExpansion

:checkPrivileges
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)

::::::::::::::::::::::::::::::::::::::::::::
:: Invoking UAC for Privilege Escalation
::::::::::::::::::::::::::::::::::::::::::::

Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
args = "ELEV " >> "%vbsGetPrivileges%"
For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
args = args ^& strArg ^& " "  >> "%vbsGetPrivileges%"
Next >> "%vbsGetPrivileges%"
UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
"%SystemRoot%\System32\WScript.exe" "%vbsGetPrivileges%" %*
exit /B

:gotPrivileges
setlocal & pushd .
cd /d %~dp0
if '%1'=='ELEV' (del "%vbsGetPrivileges%" 1>nul 2>nul  &  shift /1)

:::::::::::::::::::::::::::
::START: Run shell as admin
:::::::::::::::::::::::::::
SET PowerShellScriptPath=.\del_checkstatus.ps1
PowerShell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -InputFormat None -ExecutionPolicy Bypass -WindowStyle Hidden ""%PowerShellScriptPath%""' -Verb Runas}" -Verb Runas;