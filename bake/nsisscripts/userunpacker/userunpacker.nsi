#
#   HiSPARC user installer
#   R.Hart@nikhef.nl, NIKHEF, Amsterdam
#   Latest Revision: Aug 2013
#

!include FileFunc.nsh
!include LogicLib.nsh

SetCompressor lzma

!include ..\hs_def.nsh
!include interface.nsh

RequestExecutionLevel user

Var HisparcDir
Var UserDir
Var ConfigFile
Var Result
Var FileName

Name        "HiSPARC ${HS_USER_UNPACKER} ${USER_VERSION}"
OutFile     "${HISPARC_NSIS_RELEASE_DIR}\${HS_USER_UNPACKER}_v${USER_VERSION}.exe"
InstallDir  "$UserDir"

ShowInstDetails   show
ShowUninstDetails show

Function .onInit
  DetailPrint "user-.onInit"
  
  InitPluginsDir
  
  # Check for 32-bit or 64-bit computer
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
  StrCmp $0 "0" is32 is64
is32:
  SetRegView 32
  Goto proCeed
is64:
  SetRegView 64
  
proCeed:
  # userUnpacker needs no administrator rights
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" noReg
  ${DirState} $HisparcDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $HisparcDir does not exist!$\nUser-Installation aborted."
    Quit
  ${Endif}
  DetailPrint "HisparcDir: $HisparcDir"
  
  StrCpy $UserDir    "$HisparcDir\user"
  StrCpy $ConfigFile "$HisparcDir\persistent\configuration\config.ini"
  
  StrCpy $FileName $ConfigFile
  Call fileExists   # check if configfile exists
  Return
  
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nUser-Installation aborted."
  Quit
FunctionEnd

Function fileExists
  FileOpen $Result $FileName r
  StrCmp $Result "" noFile
  FileClose $Result
  Return
noFile:
  MessageBox MB_ICONEXCLAMATION "Cannot open $FileName!$\nUser-Installation aborted."
  Quit
FunctionEnd

Section -InstallProgs
  DetailPrint "user-InstallProgs"
  # Copy the files
  SetOutPath $HisparcDir
  SetOverwrite on
  File /r "..\..\..\user"
  # redundent check
  ${DirState} $UserDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $UserDir does not exist!$\nUser-Installation aborted."
    Quit
  ${Endif}
SectionEnd

Section -Post
  DetailPrint "user-Post"
  WriteINIStr $ConfigFile Version CurrentUser ${USER_VERSION}
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_USER_VERSION} ${USER_VERSION}
  WriteUninstaller "$HisparcDir\persistent\uninstallers\useruninst.exe"
SectionEnd

Function un.onInit

  # Check for 32-bit or 64-bit computer
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
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
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $UserDir does not exist!$\nUser-Uninstallation aborted."
    Quit
  ${Endif}
  DetailPrint "UserDir: $UserDir"
  Return
  
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nUser-Uninstallation aborted."
  Quit
FunctionEnd

Section un.Uninstall
  DetailPrint "user-un.Uninstall"
  RMDir /r /REBOOTOK "$UserDir"
  Delete "$HisparcDir\persistent\uninstallers\useruninst.exe"
  SetAutoClose true
SectionEnd