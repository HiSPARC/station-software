#########################################################################################
#
# HiSPARC NSIS user unpacker
# Code to create the user part of the HiSPARC installer
# Called from:  - ././bakescripts/bake.py
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this unpacker does (no administrator rights required):
# - Check x86 (32 bits) vs x64 (64 bits) architecture
# - Check if config.ini exists
# - Include:
#   - FileFunc.nsh
#   - LogicLib.nsh
#   - ..\hs_def.nsh
#   - interface2.nsh
#   - firewall.nsh
#
#########################################################################################
#
# Jul 2017: - Cosmetics
#           - Firewall rule for mysqld added
# Apr 2018: - Copy latest version of FTDI dll from driver installation to LabView folder
#
#########################################################################################

!include "x64.nsh"
!include FileFunc.nsh
!include LogicLib.nsh

SetCompressor lzma

!include ..\hs_def.nsh
!include interface2.nsh

RequestExecutionLevel user

Var HisparcDir
Var Result
Var UserDir
Var Architecture
Var ConfigFile
Var FileName

Name        "HiSPARC ${HS_USER_UNPACKER} ${USER_VERSION}"
OutFile     "${HISPARC_NSIS_RELEASE_DIR}\${HS_USER_UNPACKER}_v${USER_VERSION}.exe"
InstallDir  "$UserDir"

ShowInstDetails   show
ShowUninstDetails show

Function .onInit
#
# Initialise user unpacker section
  DetailPrint "user-.onInit"
  InitPluginsDir
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
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $HisparcDir does not exist!$\nUser-Installation aborted."
    Quit
  ${Endif}
  DetailPrint "HisparcDir: $HisparcDir"
  StrCpy $UserDir    "$HisparcDir\user"
  StrCpy $ConfigFile "$HisparcDir\persistent\configuration\config.ini"
  StrCpy $FileName $ConfigFile
# Check if config file exists
  Call fileExists
  Return
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nUser-Installer aborted."
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
  MessageBox MB_ICONEXCLAMATION "Cannot open $FileName!$\nUser-Installation aborted."
  Quit
FunctionEnd

Section -InstallProgs
#
# Get user installation directory
  DetailPrint "user-InstallProgs"
# Copy all files
  SetOutPath $HisparcDir
  SetOverwrite on
  File /r "..\..\..\user"
# Check whether user directory exists
  ${DirState} $UserDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $UserDir does not exist!$\nUser-Installater aborted."
    Quit
  ${Endif}
# Copy the FTDI interface dll for HiSPARC DAQ LabVIEW programme
  ${If} $Architecture == "32"
    CopyFiles "$HisparcDir\admin\ftdi_drivers\x32\i386\ftd2xx.dll" "$UserDir\hisparcdaq\ftd2xx.dll"
  ${Else}
# We need the 32-bits version of the dll since we run 32-bits LabVIEW.
# You cannot call a 64-bit dll from 32-bit LabView
    CopyFiles "$HisparcDir\admin\ftdi_drivers\x64\i386\ftd2xx.dll" "$UserDir\hisparcdaq\ftd2xx.dll"
  ${Endif}
SectionEnd

!include firewall.nsh

Section -Post
#
# Write HiSPARC-userunpacker registry parameters
  DetailPrint "user-Post"
  WriteINIStr $ConfigFile Version CurrentUser ${USER_VERSION}
# Write user version into the registry
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_USER_VERSION} ${USER_VERSION}
# Write the user uninstaller
  WriteUninstaller "$HisparcDir\persistent\uninstallers\useruninst.exe"
SectionEnd

Function un.onInit
#
# Initialise de user uninstaller; check for 32/64-bit architecture
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
# Check for 32/64-bit architecture
  StrCmp $0 "0" is32 is64
is32:
  SetRegView 32
  Goto proCeed
is64:
  SetRegView 64
proCeed:
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" noReg
  StrCpy $UserDir    "$HisparcDir\user"
  ${DirState} $UserDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $UserDir does not exist!$\nUser-Uninstallater aborted."
    Quit
  ${Endif}
  DetailPrint "UserDir: $UserDir"
  Return
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nUser-Uninstallater aborted."
  Quit
FunctionEnd

Section un.Uninstall
#
# Remove the entire user directory and reboot
  DetailPrint "user-un.Uninstall"
  RMDir /r /REBOOTOK "$UserDir"
# Remove user uninstaller
  Delete "$HisparcDir\persistent\uninstallers\useruninst.exe"
  SetAutoClose true
SectionEnd
