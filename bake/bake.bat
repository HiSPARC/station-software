@echo off
:: #########################################################################################
::
:: HiSPARC Installer Creator
:: Batch file to create the HiSPARC installer
:: Primary caller: - start bake process
:: Calls:          - bake.py
::
:: R.Hart@nikhef.nl, NIKHEF, Amsterdam
:: vaneijk@nikhef.nl, NIKHEF, Amsterdam
::
:: #########################################################################################
::
::     2013: - HiSPARC Installer
:: Jul 2017: - Cosmetics
::
:: #########################################################################################


:: Call the python bake script
call "%~dp0..\user\python\python.exe" "bakescripts\bake.py"

pause