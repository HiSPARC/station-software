#
#   HiSPARC main installer
#   R.Hart@nikhef.nl, NIKHEF, Amsterdam
#   Latest Revision: April 2012; RunStatus & HiSPARC_Registry shortcut
#

!include "FileFunc.nsh"
!include "LogicLib.nsh"

SetCompressor lzma

!define PROC                32      # 32 bits (x86) version only

!define HISPARC_VERSION     "${ADMIN_VERSION}.${USER_VERSION}"

!include ..\hs_def.nsh
!include interface2.nsh
!include variables.nsh
!include userinput.nsh

Name        "${HISPARC_NAME} ${HISPARC_VERSION}"
OutFile     "${HISPARC_NSIS_RELEASE_DIR}\hisparcInstaller_v${HISPARC_VERSION}.exe"
InstallDir  "$PROGRAMFILES\${HISPARC_NAME}"

LangString  lsWrongVersion ${LANG_ENGLISH} "HiSPARC runs only on Windows XP or 7."
LangString  lsNoAdmin      ${LANG_ENGLISH} "You have no administrator rights."
LangString  lsWrongProc    ${LANG_ENGLISH} "This distribution is for ${PROC} bits computers only."

ShowInstDetails   show
ShowUninstDetails show

Function .onInit
  DetailPrint ".OnInit"

  InitPluginsDir
  SetOutPath $PLUGINSDIR
  File /r *.ini

  # Check Windows version.
  xtInfoPlugin::IsWindowsME
  Pop $0
  xtInfoPlugin::IsWindows98
  Pop $1
  xtInfoPlugin::IsWindows95
  Pop $2

  ${If}   $0 == "true"
  ${OrIf} $1 == "true"
  ${OrIf} $2 == "true"
     MessageBox MB_ICONEXCLAMATION $(lsWrongVersion)
     Abort $(lsWrongVersion)
  ${EndIf}

  # Check if user has administrator rights.
  xtInfoPlugin::IsAdministrator
  Pop $0

  ${If} $0 == "false"
     MessageBox MB_ICONEXCLAMATION $(lsNoAdmin)
     Abort $(lsNoAdmin)
  ${EndIf}

  # Check for 32-bit computers
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
  IntCmp $0 0 is32
  IntCmp ${PROC} 64 procOk
wrongProc:
  MessageBox MB_ICONEXCLAMATION $(lsWrongProc)
  Abort $(lsWrongProc)
is32:
  IntCmp ${PROC} 32 procOk wrongProc wrongProc
procOk:

  ReadRegStr $CurVersion HKLM "${HISPARC_KEY}" ${REG_HISPARC_VERSION}
  StrCmp $CurVersion "" Install
  MessageBox MB_YESNO|MB_ICONQUESTION "It seems HiSPARC version $CurVersion is still installed.$\n\
  Do you want to continue the installation?" IDYES Install IDNO NoInstall
NoInstall:
  Quit
Install:
  Return
FunctionEnd

Function fileExists
  FileOpen $Result $FileName r
  StrCmp $Result "" nofile
  FileClose $Result
  Return
nofile:
  MessageBox MB_ICONEXCLAMATION "Cannot open $FileName!$\nMAIN-Installation aborted."
  Quit
FunctionEnd

Section -SetMainVariables
  DetailPrint "SetMainVariables"

  StrCpy $HisparcDir "$INSTDIR\hisparc"
  StrCpy $ConfigFile "$HisparcDir\persistent\configuration\config.ini"
  CreateDirectory    "$HisparcDir"
  DetailPrint        "HisparcDir: $HisparcDir"

  ${DirState} $HisparcDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: cannot create $HisparcDir !$\nMAIN-Installation aborted."
    Quit
  ${Endif}
SectionEnd

#
# Copy files to the directory on the harddisk
#
Section -CopyFilesForInstall
  DetailPrint "CopyFilesForInstall"

  SetOutPath "$HisparcDir"
  SetOverwrite on
  File /r "..\..\..\persistent"

  # Create downloads folder and copy the adminUpdater and userUnpacker into it.
  SetOutPath "$HisparcDir\persistent\downloads"
  SetOverwrite on
  File /r "..\..\releases\${HS_ADMIN_UPDATER}_v${ADMIN_VERSION}.exe" "..\..\releases\${HS_USER_UNPACKER}_v${USER_VERSION}.exe"

  # Create directory for the admin, user and main installer to put their uninstallers!
  CreateDirectory "$HisparcDir\persistent\uninstallers"

  # Copy certificate to the right location
  CopyFiles $CertZip "$HisparcDir\persistent\configuration"
SectionEnd

#
# Update the configuration file
#
Section -WriteConfigFile
  DetailPrint "WriteConfigFile"

  StrCpy $FileName $ConfigFile
  Call fileExists

  # Station settings
  WriteINIStr $ConfigFile Station       Nummer      $StationNumber
  WriteINIStr $ConfigFile Station       Password    $StationPassword
  WriteINIStr $ConfigFile Station       Certificate $CertZip
  WriteINIStr $ConfigFile Upload        LocalDBUrl  $LDBHOST

  # Connected detectors/sensors
  WriteINIStr $ConfigFile Detector      Enabled     $HasHiSPARC
  WriteINIStr $ConfigFile Weather       Enabled     $HasWeatherStation
  WriteINIStr $ConfigFile EarthMagnetic Enabled     $HasEarthMagnetic
  WriteINIStr $ConfigFile Lightning     Enabled     $HasLightning
SectionEnd

#
# Set the HiSPARC registry variables
#
Section -WriteRegKeys
  DetailPrint "WriteRegKeys"
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_PATH}            $HisparcDir
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_VOLATILE_PATH}   $HisparcDir
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_DISPLAY_NAME}    "${HISPARC_NAME}"
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HISPARC_VERSION} "${HISPARC_VERSION}"
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_ADMIN_VERSION}   ""   # set by the admin installer
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_USER_VERSION}    ""   # set by the user installer
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_STATION_NUMBER}  $StationNumber
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HAS_HISPARC}     $HasHiSPARC
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HAS_WEATHER}     $HasWeatherStation
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HAS_MAGNETIC}    $HasEarthMagnetic
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HAS_LIGHTNING}   $HasLightning
SectionEnd

#
# Call the AdminUpdater installer
#
Section -AdminInstallation
  DetailPrint "AdminInstallation"
  StrCpy $FileName "$HisparcDir\persistent\downloads\${HS_ADMIN_UPDATER}_v${ADMIN_VERSION}.exe"
  Call fileExists
  ExecWait '$HisparcDir\persistent\downloads\${HS_ADMIN_UPDATER}_v${ADMIN_VERSION}.exe /S'
SectionEnd

#
# Call the UserUnpacker installer
#
Section -UserInstallation
  DetailPrint "UserInstallation"
  StrCpy $FileName "$HisparcDir\persistent\downloads\${HS_USER_UNPACKER}_v${USER_VERSION}.exe"
  Call fileExists
  ExecWait '$HisparcDir\persistent\downloads\${HS_USER_UNPACKER}_v${USER_VERSION}.exe /S'
SectionEnd

#
# Create the user accounts. This section takes a while.
# Printing is switched off, because passwords may be shown.
#
Section -CreateUserAccounts
  DetailPrint "CreateUserAccounts"
  SetDetailsPrint none
  # admin
  ExecWait "net user ${ADMHISPARC_USERNAME} ${ADMHISPARC_PASSWORD} /add /expires:never"
  ExecWait "net localgroup Administrators ${ADMHISPARC_USERNAME} /add"
  # user
  ExecWait "net user ${HISPARC_USERNAME} ${HISPARC_PASSWORD} /add /expires:never /passwordchg:no"
  SetDetailsPrint both
SectionEnd

#
# Enable automatic logon at startup.
#
Section -AutologonEnabling
  DetailPrint "AutologonEnabling"

  StrCpy $CpuName "this computer"
  ReadRegStr $0 HKLM ${CPUNAME_KEY} ${CPV_CPUNAME}
  StrCmp $0 "" done
  StrCpy $CpuName $0
done:
  DetailPrint "- CpuName: $CpuName"
  WriteRegStr HKLM ${AUTOLOGON_KEY} ${ALV_USER_NAME}   "${HISPARC_USERNAME}"
  WriteRegStr HKLM ${AUTOLOGON_KEY} ${ALV_PASSWORD}    "${HISPARC_PASSWORD}"
  WriteRegStr HKLM ${AUTOLOGON_KEY} ${ALV_AUTO_ADMIN}  "1"
  WriteRegStr HKLM ${AUTOLOGON_KEY} ${ALV_FORCE_ADMIN} "0"
  WriteRegStr HKLM ${AUTOLOGON_KEY} ${ALV_DOMAIN_NAME} "$CpuName"
SectionEnd

#
# Add HiSPARC commands as shortcut to 'All Programs' list and
# add Startup.bat to startup folder.
#
Section -AdditionalIcons
  DetailPrint "AdditionalIcons"

  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\HiSPARC"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\StartHiSPARCSoftware.lnk" "$HisparcDir\persistent\startstopbatch\StartUserMode.bat"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\LocalDiagnosticTool.lnk"  "$HisparcDir\user\diagnostictool\run_diagnostictool.bat"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\HiSPARCDAQ.lnk"           "$HisparcDir\user\hisparcdaq\run_hisparcdaq.bat"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\DSPMon.lnk"               "$HisparcDir\user\dspmon\DSPMon.exe"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\RunStatus.lnk"            "$HisparcDir\persistent\startstopbatch\RunStatus.bat"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\HiSPARC_Registry.lnk"     "$HisparcDir\persistent\startstopbatch\HiSPARC_Registry.exe"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\Uninstall.lnk"            "$HisparcDir\persistent\uninstallers\mainuninst.exe"
  # Add shortcuts to the startup folder
  CreateShortCut  "$SMSTARTUP\StartHiSPARCSoftware.lnk"          "$HisparcDir\persistent\startstopbatch\StartUp.bat"
SectionEnd

#
# Write HiSPARC-uninstaller registry variables.
#
Section -Post
  DetailPrint "Post"
  WriteUninstaller "$HisparcDir\persistent\uninstallers\mainuninst.exe"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "DisplayName"     "$(^Name)"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "UninstallString" "$HisparcDir\persistent\uninstallers\mainuninst.exe"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "DisplayVersion"  "${HISPARC_VERSION}"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "URLInfoAbout"    "${HISPARC_WEB_SITE}"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "Publisher"       "${HISPARC_PUBLISHER}"
SectionEnd

!include uninstaller.nsh

#
# Reboot the CPU or not.
#
Section -ReBoot
  DetailPrint "ReBoot"

  AccessControl::GrantOnFile "$HisparcDir" "(BU)" "FullAccess"

  MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to restart the PC?$\n\
  On reboot Windows automatically activates the hisparc user account and DAQ." IDYES ReBoot IDNO NoReboot

ReBoot:
  ExecWait "shutdown -r -f -t 0"
NoReboot:
SectionEnd
