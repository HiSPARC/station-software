#########################################################################################
#
# HiSPARC parameters and definitions for the main installer
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Included in hisparcinstaller.nsi
# Define:
# - Parameters
# - HiSPARC Windows accounts
# - Windows 10 specific key(s)
#
#########################################################################################
#
# Jul 2017: - Add variable 'WinVersion'
#           - Introduce uniform naming convention service directories
#           - Add key to disable LockScreen (Windows 10 specific)
# Feb 2019: - Replaced $HasLightning by $HasLightningDetector
#
#########################################################################################

#
# General parameters
Var HisparcDir
Var Result
Var CertZip
Var FileName
Var ConfigFile
Var StationNumber
Var StationPassword
Var LDBHOST
Var HasHiSPARC
Var HasWeatherStation
Var HasLightningDetector
Var Program
Var CpuName
Var OkVersion
Var RegVersion
Var TmpVersion
Var WinVersion
Var CurVersion

#
# Registry key for (global) environment variables
!define ENVIRONMENT_KEY     "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"

#
# Windows accounts
!define ADMHISPARC_USERNAME "admhisparc"
!define HISPARC_USERNAME    "hisparc"

#
# Registry key for computer names
!define CPUNAME_KEY         "System\CurrentControlSet\Control\ComputerName\ActiveComputerName"
!define CPV_CPUNAME         "ComputerName"

#
# Registry key for autologon and variables
!define AUTOLOGON_KEY       "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
!define ALV_USER_NAME       "DefaultUserName"
!define ALV_PASSWORD        "DefaultPassword"
!define ALV_AUTO_ADMIN      "AutoAdminLogon"
!define ALV_FORCE_ADMIN     "ForceAdminLogon"
!define ALV_DOMAIN_NAME     "DefaultDomainName"
