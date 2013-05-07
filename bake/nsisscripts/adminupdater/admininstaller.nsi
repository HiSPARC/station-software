#
#   HiSPARC admin installer
#   R.Hart@nikhef.nl, NIKHEF, Amsterdam
#   Latest Revision: Aug 2012
#

!include FileFunc.nsh
!include LogicLib.nsh

SetCompressor lzma

!include ..\hs_def.nsh
!include interface.nsh
!include variables.nsh

Name        "HiSPARC ${HS_ADMIN_UPDATER} ${ADMIN_VERSION}"
OutFile     "${HISPARC_NSIS_RELEASE_DIR}\${HS_ADMIN_UPDATER}_v${ADMIN_VERSION}.exe"
InstallDir  "$AdminDir"

ShowInstDetails   show
ShowUninstDetails show

Function .onInit
  DetailPrint "admin-.onInit"
  
  InitPluginsDir
  # check if user has administrator rights
  xtInfoPlugin::IsAdministrator
  Pop $0
  ${If} $0 == "false"
    MessageBox MB_ICONEXCLAMATION "You have no administrator rights!$\nAdmin-Installation aborted."
    Quit
  ${EndIf}
  
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" noReg
  ${DirState} $HisparcDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $HisparcDir does not exist!$\nAdmin-Installation aborted."
    Quit
  ${Endif}
  DetailPrint "HisparcDir: $HisparcDir"
  
  StrCpy $AdminDir   "$HisparcDir\admin"
  StrCpy $ConfigFile "$HisparcDir\persistent\configuration\config.ini"
  
  # Check for 32-bit or 64-bit computer
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
  StrCmp $0 "0" is32
  StrCpy $OpenVpnDir "$AdminDir\openvpn64"
  GoTo proCeed
is32:
  StrCpy $OpenVpnDir "$AdminDir\openvpn32"
proCeed:
  DetailPrint "OpenVpnDir: $OpenVpnDir"
  
  StrCpy $FileName $ConfigFile
  Call fileExists   # check if configfile exists
  
  ReadINIStr $CertZip "$ConfigFile" "Station" "Certificate"
  StrCpy $FileName $CertZip
  Call fileExists   # check if certificate exists
  Return
  
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nAdmin-Installation aborted."
  Quit
FunctionEnd

Function fileExists
  FileOpen $Result $FileName r
  StrCmp $Result "" noFile
  FileClose $Result
  Return
noFile:
  MessageBox MB_ICONEXCLAMATION "Cannot open $FileName!$\nAdmin-Installation aborted."
  Quit
FunctionEnd

#
# Copy all files to the install directory
#
Section -InstallProgs
  DetailPrint "admin-InstallProgs"
  # copy the files
  SetOutPath "$HisparcDir"
  SetOverwrite on
  File /r "..\..\..\admin"
  # redundent check
  ${DirState} $AdminDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $AdminDir does not exist!$\nAdmin-Installation aborted."
    Quit
  ${Endif}
SectionEnd

!include install.nsh
!include firewall.nsh

#
# Post admin installation
#
Section -Post
  DetailPrint "admin-Post"
  # set admin version
  WriteINIStr $ConfigFile Version CurrentAdmin ${ADMIN_VERSION}
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_ADMIN_VERSION} ${ADMIN_VERSION}
  # LabVIEW
  ReadRegStr $NIdir HKLM "${LABVIEW_KEY}" ${LABVIEW_DIR}
  AccessControl::GrantOnFile "$NIdir" "(BU)" "FullAccess"
  # admin uninstaller
  WriteUninstaller "$HisparcDir\persistent\uninstallers\adminuninst.exe"
SectionEnd

!include uninstall.nsh
