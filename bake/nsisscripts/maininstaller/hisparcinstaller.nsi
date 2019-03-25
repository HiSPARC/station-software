#########################################################################################
#
# HiSPARC NSIS main (un)installer for full installation package
# Called from:  - ././bakescripts/bake.py
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this installer does:
# - Determine Windows OS version and 32/64 bit architecture (for registry)
# - Check administrator rights (required)
# - Create installation directory (Program Files(x86)/HiSPARC)
# - Create directory (sub)structure and copy all files
# - Write registry keys and execute adminUpdater and userUnpacker
# - Create Windows accounts 'admhisparc' and 'hisparc'
# - Set autologon for user 'hisparc'
# - Add shortcuts to 'Start' menu
# - Includes:
#   - FileFunc.nsh
#   - LogicLib.nsh
#   - ..\hs_def.nsh
#   - ..\password.nsh
#   - interface2.nsh
#   - variables.nsh
#   - userinput.nsh
#   - uninstaller.nsh
#
#########################################################################################
#
# Apr 2012: - RunStatus & HiSPARC_Registry shortcut
# Jun 2012: - Added HISPARC_ROOT environment variable & grouped set of shortcuts
#             Prevent Windows password from expiring
# Aug 2012: - Uninstaller cleaned and checked, labels renamed
# Jan 2013: - Release number part of version
# Aug 2013: - 64-bit architecture support
# Sep 2015: - DAQ and Weather executables with spaces, :-(
#             HiSPARC moved from $INSTDIR\hisparc to $INSTDIR
# Aug 2016: - Extended check on Windows version
# Sep 2016: - Power management pc and monitor ---> never go to sleep
#           - Set NoLockScreen register to 1 (for Windows 10)
# Jul 2017: - Windows OS version determination updated
#           - TrimbleVTS added for new GPS module control
#           - Removed option 'expert' operation of DAQ software
# Apr 2018: - Admin version 9 and higher: Windows 10 only!
#           - Serialise startup of applications; interval: 1 second
#           - Modified reboot menu
# Feb 2019: - Lightning Detector LabView software added
#           - Replaced $HasHiSPARC by $HasDAQ
#
#########################################################################################

!include "FileFunc.nsh"
!include "LogicLib.nsh"

SetCompressor lzma

!define HISPARC_VERSION     "${ADMIN_VERSION}.${USER_VERSION}.${RELEASE}"
!include ..\hs_def.nsh
!include ..\password.nsh
!include interface2.nsh
!include variables.nsh
!include userinput.nsh

Name        "${HISPARC_NAME} ${HISPARC_VERSION}"
OutFile     "${HISPARC_NSIS_RELEASE_DIR}\hisparcInstaller_v${HISPARC_VERSION}.exe"
InstallDir  "$PROGRAMFILES\${HISPARC_NAME}"

ShowInstDetails   show
ShowUninstDetails show

Section -SetMainVariables
#
# Get main installation directory
  DetailPrint "SetMainVariables"
  StrCpy $HisparcDir "$INSTDIR"
# Path to the HiSPARC configuration file
  StrCpy $ConfigFile "$HisparcDir\persistent\configuration\config.ini"
# Create the HiSPARC directory
  CreateDirectory    "$HisparcDir"
  DetailPrint        "HisparcDir: $HisparcDir"
  ${DirState} $HisparcDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: cannot create $HisparcDir !$\nMAIN-Installation aborted."
    Quit
  ${Endif}
SectionEnd

Section -CopyFilesForInstall
#
# Create directory (sub)structure and copy all files
  DetailPrint "CopyFilesForInstall"
  SetOutPath "$HisparcDir"
  SetOverwrite on
# Copy persistent folder
  File /r "..\..\..\persistent"
# Copy the adminUpdater and userUnpacker into the download folder
  SetOutPath "$HisparcDir\persistent\downloads"
  SetOverwrite on
  File /r "..\..\releases\${HS_ADMIN_UPDATER}_v${ADMIN_VERSION}.exe" "..\..\releases\${HS_USER_UNPACKER}_v${USER_VERSION}.exe"
# Create directory for the admin, user and main uninstallers
  CreateDirectory "$HisparcDir\persistent\uninstallers"
# Copy (unique) station certificate to the right location
  CopyFiles $CertZip "$HisparcDir\persistent\configuration"
SectionEnd

Section -WriteConfigFile
#
# Get the configuration parameters of the station
  DetailPrint "WriteConfigFile"
  StrCpy $FileName $ConfigFile
  Call fileExists
# Station specific parameters
  WriteINIStr $ConfigFile Station       Nummer      $StationNumber
  WriteINIStr $ConfigFile Station       Password    $StationPassword
  WriteINIStr $ConfigFile Station       Certificate $CertZip
  WriteINIStr $ConfigFile Upload        LocalDBUrl  $LDBHOST
# Active detectors/sensors attached to the station
  WriteINIStr $ConfigFile DAQ           Enabled     $HasDAQ
  WriteINIStr $ConfigFile Weather       Enabled     $HasWeather
  WriteINIStr $ConfigFile Lightning     Enabled     $HasLightning
SectionEnd

Section -WriteRegKeys
#
# Set the HiSPARC registry and global environment variable
  DetailPrint "WriteRegKeys"
# HiSPARC registry keys
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_PATH}            $HisparcDir
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_VOLATILE_PATH}   $HisparcDir
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_DISPLAY_NAME}    "${HISPARC_NAME}"
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HISPARC_VERSION} "${HISPARC_VERSION}"
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_ADMIN_VERSION}   ""   # set by the admin installer
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_USER_VERSION}    ""   # set by the user installer
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_RELEASE}         "${RELEASE}"
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_RELEASE_DATE}    "${RELEASE_DATE}"
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_STATION_NUMBER}  $StationNumber
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HAS_DAQ}         $HasDAQ
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HAS_WEATHER}     $HasWeather
  WriteRegStr HKLM "${HISPARC_KEY}" ${REG_HAS_LIGHTNING}   $HasLightning
# HiSPARC environment parameter
  WriteRegStr HKLM "${ENVIRONMENT_KEY}" ${HISPARC_ROOT}    $HisparcDir
SectionEnd

Section -AdminInstallation
#
# Execute the adminUpdater
  DetailPrint "AdminInstallation"
  StrCpy $FileName "$HisparcDir\persistent\downloads\${HS_ADMIN_UPDATER}_v${ADMIN_VERSION}.exe"
  Call fileExists
  StrCpy $Program $FileName
  ExecWait '"$Program" /S' $Result
SectionEnd

Section -UserInstallation
#
# Execute the userUnpacker
  DetailPrint "UserInstallation"
  StrCpy $FileName "$HisparcDir\persistent\downloads\${HS_USER_UNPACKER}_v${USER_VERSION}.exe"
  Call fileExists
  StrCpy $Program $FileName
  ExecWait '"$Program" /S' $Result
SectionEnd

Section -CreateUserAccounts
#
# Create the Windows accounts. This section takes a while.
# Printing is switched off, because passwords may be shown...
  DetailPrint "CreateUserAccounts"
  SetDetailsPrint none
# Admin: admhisparc
  ExecWait "net user ${ADMHISPARC_USERNAME} ${ADMHISPARC_PASSWORD} /add /expires:never"
  ExecWait "net localgroup Administrators ${ADMHISPARC_USERNAME} /add"
# User: hisparc
  ExecWait "net user ${HISPARC_USERNAME} ${HISPARC_PASSWORD} /add /expires:never /passwordchg:no"
# Set accounts so that passwords never expire (RH: June 8 2012)
  ExecWait "net accounts /maxpwage:unlimited"
  SetDetailsPrint both
SectionEnd

Section -AutologonEnabling
#
# Enable automatic logon at startup
  DetailPrint "AutologonEnabling"
# Obtain computer name
  StrCpy $CpuName "this computer"
  ReadRegStr $0 HKLM "${CPUNAME_KEY}" ${CPV_CPUNAME}
  StrCmp $0 "" wrAutoLogon
  StrCpy $CpuName $0
wrAutoLogon:
  DetailPrint "- CpuName: $CpuName"
  WriteRegStr HKLM "${AUTOLOGON_KEY}" ${ALV_USER_NAME}   "${HISPARC_USERNAME}"
  WriteRegStr HKLM "${AUTOLOGON_KEY}" ${ALV_PASSWORD}    "${HISPARC_PASSWORD}"
  WriteRegStr HKLM "${AUTOLOGON_KEY}" ${ALV_AUTO_ADMIN}  "1"
  WriteRegStr HKLM "${AUTOLOGON_KEY}" ${ALV_FORCE_ADMIN} "0"
  WriteRegStr HKLM "${AUTOLOGON_KEY}" ${ALV_DOMAIN_NAME} "$CpuName"
SectionEnd

Section -AdditionalIcons
#
# Add HiSPARC commands as shortcut to 'All Programs' list
# and add Startup.bat to startup folder
  DetailPrint "AdditionalIcons"
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\HiSPARC"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\Start HiSPARC software.lnk"  "$HisparcDir\persistent\startstopbatch\StartUserMode.bat"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\HiSPARC directory.lnk"       "%windir%\explorer.exe" "$HisparcDir"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\Run status.lnk"              "$HisparcDir\persistent\startstopbatch\RunStatus.bat"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\Diagnostics.lnk"             "$HisparcDir\user\diagnostictool\run_diagnostictool.bat"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\Registry.lnk"                "$HisparcDir\persistent\startstopbatch\HiSPARC_Registry.exe"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\DSPMon.lnk"                  "$HisparcDir\user\dspmon\DSPMon.exe"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\TrimbleVTS.lnk"              "$HisparcDir\user\dspmon\TrimbleVTS.exe"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\HiSPARC DAQ.lnk"             "$HisparcDir\user\hisparcdaq\HiSPARC DAQ.exe"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\HiSPARC Weather.lnk"         "$HisparcDir\user\hisparcweather\HiSPARC Weather Station.exe"
  CreateShortCut  "$SMPROGRAMS\HiSPARC\HiSPARC Lightning.lnk"       "$HisparcDir\user\hisparclightning\HiSPARC Lightning Detector.exe"
# Add uninstaller shortcut to startup menu
  Sleep 3000
  CreateShortCut  "$SMPROGRAMS\HiSPARC\HiSPARC Uninstall.lnk"       "$HisparcDir\persistent\uninstallers\mainuninst.exe"
# Add shortcut to the startup folder; after autologon the HiSPARC software will automatically be launched
  CreateShortCut  "$SMSTARTUP\Start HiSPARC software.lnk"           "$HisparcDir\persistent\startstopbatch\StartUp.bat"
SectionEnd

Section -Post
#
# Write HiSPARC-uninstaller registry parameters
  DetailPrint "Post"
  WriteUninstaller "$HisparcDir\persistent\uninstallers\mainuninst.exe"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "DisplayName"     "$(^Name)"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "UninstallString" "$HisparcDir\persistent\uninstallers\mainuninst.exe"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "DisplayVersion"  "${HISPARC_VERSION}"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "URLInfoAbout"    "${HISPARC_WEB_SITE}"
  WriteRegStr HKLM "${HISPARC_UNINST_KEY}" "Publisher"       "${HISPARC_PUBLISHER}"
SectionEnd

!include uninstaller.nsh

Section -ReBoot
#
# Chose to (not) reboot the PC...
  DetailPrint "ReBoot"
  AccessControl::GrantOnFile "$HisparcDir" "(BU)" "FullAccess"
  HideWindow
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you wish to restart the PC?$\n\
  On reboot Windows automatically activates the hisparc user account and DAQ." IDYES reBoot IDNO noReboot
reBoot:
  ExecWait "shutdown /g /f -t 0"
noReboot:
SectionEnd

Function GetWindowsVersion
#
# Determine which version of the desktop Windows OS is running
# As of Admin version 9, only Windows 10 or higher accepted!
  ClearErrors
# Set Windows OS version to be 'invalid'  
  StrCpy $OkVersion "false"
# Check if Windows 10 family (CurrentMajorVersionNumber is new introduced in Windows 10)
  ReadRegStr $RegVersion HKLM \
  "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentMajorVersionNumber
  StrCmp $RegVersion '' 0 lbl_winnt
  ClearErrors
# OS version is NT family?  
  ReadRegStr $RegVersion HKLM \
  "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion
  IfErrors 0 lbl_winnt
# OS is not Windows NT family...
  ReadRegStr $RegVersion HKLM \
  "SOFTWARE\Microsoft\Windows\CurrentVersion" VersionNumber
  StrCpy $TmpVersion $RegVersion 1
  StrCmp $TmpVersion '4' 0 lbl_error
  StrCpy $TmpVersion $RegVersion 3
  StrCmp $TmpVersion '4.0' lbl_win32_95
  StrCmp $TmpVersion '4.9' lbl_win32_ME lbl_win32_98
lbl_win32_95:
  StrCpy $WinVersion '95'
  Goto lbl_done
lbl_win32_98:
  StrCpy $WinVersion '98'
  Goto lbl_done
lbl_win32_ME:
  StrCpy $WinVersion 'ME'
  Goto lbl_done
lbl_winnt:
# OS is Windows NT family...
  StrCpy $TmpVersion $RegVersion 1
  StrCmp $TmpVersion '3' lbl_winnt_x
  StrCmp $TmpVersion '4' lbl_winnt_x
  StrCpy $TmpVersion $RegVersion 3
  StrCmp $TmpVersion '5.0' lbl_winnt_2000
  StrCmp $TmpVersion '5.1' lbl_winnt_XP
  StrCmp $TmpVersion '5.2' lbl_winnt_2003
  StrCmp $TmpVersion '5.3' lbl_winnt_vista
  StrCmp $TmpVersion '6.1' lbl_winnt_7
  StrCmp $TmpVersion '6.2' lbl_winnt_8
  StrCmp $TmpVersion '6.3' lbl_winnt_81
  StrCmp $TmpVersion '10' lbl_winnt_10
# Check remainder; Windows 10.0?
  StrCpy $TmpVersion $RegVersion 4
  StrCmp $R1 '10.0' lbl_winnt_10
  Goto lbl_error
# Windows version is now determined...
  lbl_winnt_x:
  StrCpy $WinVersion "NT $RegVersion" 6
  Goto lbl_done
lbl_winnt_2000:
  StrCpy $WinVersion '2000'
  Goto lbl_done
lbl_winnt_XP:
  StrCpy $WinVersion 'XP'
  Goto lbl_done
lbl_winnt_2003:
  StrCpy $WinVersion '2003'
  Goto lbl_done
lbl_winnt_vista:
  StrCpy $WinVersion 'Vista'
  Goto lbl_done
lbl_winnt_7:
  StrCpy $WinVersion '7'
  Goto lbl_done
lbl_winnt_8:
  StrCpy $WinVersion '8'
  Goto lbl_done
lbl_winnt_81:
  StrCpy $WinVersion '8.1'
  Goto lbl_done
# Admin version 9 and higher: only Windows 10 and higher accepted...
lbl_winnt_10:
  StrCpy $WinVersion '10.0'
  StrCpy $OkVersion "true"
  Goto lbl_done
lbl_error:
  StrCpy $WinVersion $RegVersion
  StrCpy $OkVersion "unknown"
lbl_done:
FunctionEnd

Function fileExists
#
# Check if the file exists
  FileOpen $Result $FileName r
  StrCmp $Result "" noFile
  FileClose $Result
  Return
noFile:
  MessageBox MB_ICONEXCLAMATION "Cannot open $FileName!$\nMain-Installation aborted."
  Quit
FunctionEnd

Function .onInit
#
# Initialise main installer section
  DetailPrint ".OnInit"
  InitPluginsDir
  SetOutPath $PLUGINSDIR
  File /r *.ini
# mainIstaller requires administrator rights
  xtInfoPlugin::IsAdministrator
  Pop $0
  ${If} $0 == "false"
    MessageBox MB_ICONEXCLAMATION "You have no administrator rights!$\nMain-Installation aborted."
    Quit
  ${EndIf}
# mainIstaller requires elevated administrator rights
  UserInfo::GetAccountType
  Pop $0
  ${If} $0 != "admin" ;Require elevated admin rights on NT4+
    MessageBox MB_ICONEXCLAMATION "Windows UAC shield requires elevated administrator rights - run as administrator -!$\nMain-Installation aborted."
    Quit
  ${EndIf}
# Check Windows OS version
  Call GetWindowsVersion
  StrCmp $OkVersion "true" proCeed1
  StrCmp $OkVersion "false" wrVersion unkVersion
wrVersion:
# Non-valid OS version
  MessageBox MB_ICONEXCLAMATION "HiSPARC runs only on Windows OS 10 or higher, not on $WinVersion"
  Goto noInstall
unkVersion:
# Unknown OS version
  MessageBox MB_YESNO|MB_ICONQUESTION "The Windows OS version $WinVersion is unknown.$\n\
  Do you wish to continue the installation process?" IDYES proCeed1 IDNO noInstall
proCeed1:
# Check for 32/64-bit architecture
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
  StrCmp $0 "0" is32 is64
is32:
  SetRegView 32
  Goto proCeed2
is64:
  SetRegView 64
proCeed2:
  ReadRegStr $CurVersion HKLM "${HISPARC_KEY}" ${REG_HISPARC_VERSION}
  StrCmp $CurVersion "" Install
  MessageBox MB_YESNO|MB_ICONQUESTION "It seems HiSPARC version $CurVersion is still installed.$\n\
  Do you want to continue the installation?" IDYES inStall IDNO noInstall
noInstall:
  Quit
inStall:
# Keep pc and monitor alive for all accounts!
  ExecWait "powercfg -h off"
  ExecWait "powercfg -change -standby-timeout-ac 0"
  ExecWait "powercfg -change -monitor-timeout-ac 0"
# Serialise startup of applications; introduce delay of 1 second
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Explorer\Serialize" "Startupdelayinmsec" 0x00001000
FunctionEnd
