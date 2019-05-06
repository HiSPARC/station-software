#########################################################################################
#
# HiSPARC admin installer: variables.nsh
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Included in admininstaller.nsi
# Define:
# - Parameters
# - Services and services keys
# - Windows 10 specific key(s)
#
#########################################################################################
#
#     2013: - First version
# Jul 2017: - Introduce uniform naming convention service directories and executables
#           - Add key to disable LockScreen (Windows 10 specific)
# Sep 2017: - Prolific PL2303 and SiLabs CP210x VCP drivers for Davis weather station
# Apr 2018: - Visual C++ Redistributable Packages for Visual Studio 2013 added (ODBC)
#           - Changed Windows 10 driver install utility
#           - IVI-Foundation removal tool version 5.8.0 added for NI-Visa
#           - Generic (un)installer name added
# Apr 2019: - Add Scheduled Task(s) parameters
#           - quickstart folder added
#
#########################################################################################

#
# General parameters
Var HisparcDir
Var Architecture
Var AdminDir
Var Message
Var FolderName
Var FileName
Var Result

#
# Generic (un)installer name
!define INSTALL_BAT         "Installer"
!define UNINSTALL_BAT       "Uninstaller"

#
# OpenVPN (and TAP - Virtual Ethernet Adapter)
Var OpenVPNDir
Var ConfigFile
Var CertZip
!define NETVersion          "4.0"
!define NETInstaller        "dotNetFx40_Full_x86_x64.exe"
!define NET_KEY             "SOFTWARE\Microsoft\NET Famework Setup\NDP\v4\Full"
!define VPN_SERVICENAME     "OpenVPNService"
!define VPN_EXENAME         "openvpn"
!define OPENVPN_KEY         "SOFTWARE\OpenVPN"
!define OPENVPNMS_KEY       "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\OpenVPN"
!define TAP_EXENAME         "devcon"
!define TAP                 "tap0901"
!define TAPDRV              "${TAP}.sys"
!define TAPCAT              "${TAP}.cat"

#
# TightVNC
Var TightVNCDir
!define VNC_SERVICENAME     "tvnserver"
!define VNC_EXENAME         "tvnserver"
!define TIGHTVNC_KEY        "SOFTWARE\TightVNC"
!define TVNCSERVER_KEY      "SOFTWARE\TightVNC\Server"
!define TVNCCOMPONENTS_KEY  "SOFTWARE\TightVNC\Components"

#
# Nagios Client++
Var NSCPDir
!define NSCP_SERVICENAME    "nscp"
!define NSCP_EXENAME        "NSClient++"
!define NSCP_ININAME        "nsclient"

#
# ODBC database connector for Windows
Var ODBCDir
!define VCRE32_EXENAME      "vcredist_x86"
!define VCRE64_EXENAME      "vcredist_x64"
!define ODBCDRV             "MySQL ODBC 5.3 Driver"
!define ODBC_KEY            "SOFTWARE\ODBC\ODBC.INI\buffer"
!define ODBCDS_KEY          "SOFTWARE\ODBC\ODBC.INI\ODBC Data Sources"
!define ODBCDRVPATH         "C:\WINDOWS\system32\myodbc5.dll"
!define BDBHOST             "localhost"

#
# National Instruments Run Time Engine
Var NIRTEDir
Var NIDir
!define NIRTE_EXENAME       "setup"
!define LABVIEW_KEY         "SOFTWARE\National Instruments\Common\Installer"
!define LABVIEW_DIR         "NIDIR"
!define VISA_EXENAME        "VisaClean"

#
# FTDI USB drivers for Windows
Var FTDIDir
!define FTDI_EXENAME        "dpinst"
!define FTDI_ENUM_VALUE     "01"
!define FTDI_ENUM_KEY       "SYSTEM\CurrentControlSet\Control\UsbFlags"
!define FTDI_ENUM_REG1      "IgnoreHWSerNum04036001"
!define FTDI_ENUM_REG2      "IgnoreHWSerNum04036010"

#
# Delprof2
Var DelProfDir
!define DELPROF_EXENAME     "DelProf2"

#
# PL2303
Var PL2303Dir
!define PL2303_EXENAME      "PL2303"

#
# CP210X
Var CP210XDir
!define CP210X_EXENAME      "CP210x"

#
# Utilities
Var UTILDir

#
# Create/delete task(s) for Windows Task Scheduler
Var TASKDir
!define TASK1_CREATE        "cre_checkstatus"
!define TASK1_EXENAME       "CheckStatus"
!define TASK1_DELETE        "del_checkstatus"

#
# Windows 10 specific
!define LOCKSCREEN_KEY      "SOFTWARE\Policies\Microsoft\Windows\Personalization"
!define LOCKSCREEN_REG      "NoLockScreen"
