#
#   HiSPARC user installer
#   R.Hart@nikhef.nl, NIKHEF, Amsterdam
#   Latest Revision: Oct 2011
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
  
  # userUnpacker needs no administrator rights
  
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" nopath
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
  
nopath:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nUser-Installation aborted."
  Quit
FunctionEnd

Function fileExists
  FileOpen $Result $FileName r
  StrCmp $Result "" nofile
  FileClose $Result
  Return
nofile:
  MessageBox MB_ICONEXCLAMATION "Cannot open $FileName!$\nUser-Installation aborted."
  Quit
FunctionEnd

Section -InstallProgs
  DetailPrint "user-InstallProgs"
  
  # Copy the files
  SetOutPath $HisparcDir
  SetOverwrite on
  File /r "..\..\..\user"
  
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

Function un.onUninstSuccess
  # nothing to do
FunctionEnd

Function un.onInit
  # nothing to do
FunctionEnd

Section un.Uninstall
  DetailPrint "user-un.Uninstall"
  
  RMDir /r /REBOOTOK "$UserDir"
  Delete "$HisparcDir\persistent\uninstallers\useruninst.exe"
  SetAutoClose true
SectionEnd