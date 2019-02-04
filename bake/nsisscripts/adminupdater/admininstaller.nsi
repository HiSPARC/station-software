#########################################################################################
#
# HiSPARC NSIS admin installer
# Code to create the admin part of the HiSPARC installer
# Called from:  - ././bakescripts/bake.py
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this installer does:
# - Create "admin" and post admin parts of installer
# - Check administrator rights
# - Check x32 (32 bits) vs x64 (64 bits) architecture
# - Check if config.ini exists
# - Check if station (unique) certificate exists
# - Copy all files into installation directory
# - Include:
#   - ..\hs_def.nsh
#   - ..\password.nsh
#   - interface2.nsh
#   - variables.nsh
#   - services, drivers and utilities
#   - firewall.nsh
#
#########################################################################################
#
# Aug 2013: - Some applications still use the 32-bit registry
# Aug 2016: - Set NoLockScreen register to 1 (Windows 10 specific)
# Jul 2017: - Introduce uniform naming convention service directories
#           - Renamed interface ---> interface2
# Oct 2017  - Drivers included for Davis WeatherLinks (Serial and USB)
#           - NI-RTE (a dedicated installer in LabView is created)             (x32)
#
#########################################################################################

!include "x64.nsh"
!include FileFunc.nsh
!include LogicLib.nsh

SetCompressor lzma

!include ..\hs_def.nsh
!include ..\password.nsh
!include interface2.nsh
!include variables.nsh

Name        "HiSPARC ${HS_ADMIN_UPDATER} ${ADMIN_VERSION}"
OutFile     "${HISPARC_NSIS_RELEASE_DIR}\${HS_ADMIN_UPDATER}_v${ADMIN_VERSION}.exe"
InstallDir  "$AdminDir"

ShowInstDetails   show
ShowUninstDetails show

Function .onInit
#
# Initialise admin installer section
  DetailPrint "admin-.onInit"
  InitPluginsDir
# AdminInstaller requires administrator rights
  xtInfoPlugin::IsAdministrator
  Pop $0
  ${If} $0 == "false"
    MessageBox MB_ICONEXCLAMATION "You have no administrator rights!$\nAdmin-Installer aborted."
    Quit
  ${EndIf}
# Check for 32/64-bit architecture
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
  StrCmp $0 "0" is32 is64
is32:
  SetRegView 32
  StrCpy $Architecture "32"
  Goto proCeed
is64:
  SetRegView 64
  StrCpy $Architecture "64"
proCeed:
# Get HiSPARC directory name and path
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" noReg
  ${DirState} $HisparcDir $Result
# Check if HisparcDir exists
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $HisparcDir does not exist!$\nAdmin-Installer aborted."
    Quit
  ${Endif}
  DetailPrint "HisparcDir: $HisparcDir"
  StrCpy $AdminDir   "$HisparcDir\admin"
  StrCpy $ConfigFile "$HisparcDir\persistent\configuration\config.ini"
  StrCpy $FileName $ConfigFile
# Check if config file exists
  Call fileExists
# Read the station specific (unique) certificate
  ReadINIStr $CertZip "$ConfigFile" "Station" "Certificate"
  StrCpy $FileName $CertZip
# Check if station certificate exists
  Call fileExists  
# Get the service, drivers and utility directories...
  ${If} $Architecture == "32"
    StrCpy $OpenVPNDir "$AdminDir\openvpn\x32"
    StrCpy $TightVNCDir "$AdminDir\tightvnc\x32"
    StrCpy $NSCPDir "$AdminDir\nsclientpp\x32"
    StrCpy $ODBCDir "$AdminDir\odbcconnector\x32"
    StrCpy $NIRTEDir "$AdminDir\nirte\x32"
    StrCpy $FTDIDir "$AdminDir\ftdi_drivers\x32"
    StrCpy $DelProfDir "$AdminDir\delprof2\x32"
    StrCpy $PL2303Dir "$AdminDir\pl2303"
    StrCpy $CP210XDir "$AdminDir\cp210x\x32"
    StrCpy $UtilDir "$AdminDir\utilities"
  ${Else}
    StrCpy $OpenVPNDir "$AdminDir\openvpn\x64"
    StrCpy $TightVNCDir "$AdminDir\tightvnc\x64"
    StrCpy $NSCPDir "$AdminDir\nsclientpp\x64"
    StrCpy $ODBCDir "$AdminDir\odbcconnector\x32"
    StrCpy $NIRTEDir "$AdminDir\nirte\x32"
    StrCpy $FTDIDir "$AdminDir\ftdi_drivers\x64"
    StrCpy $DelProfDir "$AdminDir\delprof2\x32"
    StrCpy $PL2303Dir "$AdminDir\pl2303"
    StrCpy $CP210XDir "$AdminDir\cp210x\x64"
    StrCpy $UtilDir "$AdminDir\utilities"
  ${Endif}
  DetailPrint "OpenVPNDir: $OpenVPNDir"
  DetailPrint "TightVNCDir: $TightVNCDir"
  DetailPrint "NSCPDir: $NSCPDir"
  DetailPrint "ODBCDir: $ODBCDir"
  DetailPrint "NIRTEDir: $NIRTEDir"
  DetailPrint "FTDIDir: $FTDIDir"
  DetailPrint "DelProfDir: $DelProfDir"
  DetailPrint "PL2303Dir: $PL2303Dir"
  DetailPrint "CP210XDir: $CP210XDir"
  DetailPrint "UtilDir: $UtilDir"
  Return
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nAdmin-Installer aborted."
  Quit
FunctionEnd

Function fileExists
#
# Check if the file exists
  FileOpen $Result $FileName r
  StrCmp $Result "" noFile
  FileClose $Result
  Return
noFile:
  MessageBox MB_ICONEXCLAMATION "Cannot open $FileName!$\nAdmin-Installation aborted."
  Quit
FunctionEnd

Section -InstallProgs
#
# Get admin installation directory
  DetailPrint "admin-InstallProgs"
# Copy all files
  SetOutPath "$HisparcDir"
  SetOverwrite on
  File /r "..\..\..\admin"
# Check whether admin directory exists
  ${DirState} $AdminDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $AdminDir does not exist!$\nAdmin-Installer aborted."
    Quit
  ${Endif}
SectionEnd

!include install.nsh
!include firewall.nsh

Section -Post
#
# Write HiSPARC-admin registry parameters
  DetailPrint "admin-Post"
# Write admin version into the registry
  WriteINIStr $ConfigFile Version CurrentAdmin ${ADMIN_VERSION}
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_ADMIN_VERSION} ${ADMIN_VERSION}
# National Instruments Run Time Engine access control
  ReadRegStr $NIDir HKLM "${LABVIEW_KEY}" ${LABVIEW_DIR}
  AccessControl::GrantOnFile "$NIDir" "(BU)" "FullAccess"
# Write NoLockScreen registry key relevant for Windows 10 only
  WriteRegDWORD HKLM "${LOCKSCREEN_KEY}" ${LOCKSCREEN_REG} "1"
# Write the admin uninstaller
  WriteUninstaller "$HisparcDir\persistent\uninstallers\adminuninst.exe"
SectionEnd

!include uninstall.nsh
