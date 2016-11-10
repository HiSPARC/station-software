#
#   uninstaller.nsh ------
#   Create the main uninstaller.
#   R.Hart@nikhef.nl, Nikhef, Amsterdam
#   Sep 2016: - OpenVPN version 2.3.12 now for 32 and 64 bits
#             - OpenVPN and TAP-Windows in separate folders
#             - Account profiles can only be removed when all user (daughter-)processes have been killed!
#             - Introduced Delprof2 to remove account profiles
#

Function un.onInit
  DetailPrint "un.onInit"
  
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
  StrCmp $0 "0" is32 is64
is32:
  SetRegView 32
  Goto proCeed
is64:
  SetRegView 64

proCeed:
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" noHomedir 
  ${DirState} $HisparcDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "Folder $\"$HisparcDir$\" does not exist!$\nUninstallation canceled."
    Quit
  ${Endif}

  GetFullPathName $INSTDIR $INSTDIR\..\..\..
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES removeHisparc IDNO keepHisparc
keepHisparc:
  Abort 
removeHisparc:
  Return
noHomedir:
  MessageBox MB_ICONEXCLAMATION "Registry entry $\"${REG_PATH}$\" not set or defined!$\nUninstallation canceled."
  Quit
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to reboot the system now?" IDYES rebootPC IDNO noReboot
rebootPC:
  ExecWait "shutdown -r -f -t 0"
noReboot:
FunctionEnd

#
# Uninstall HiSPARC in one big Section
#
Section un.RemoveHisparc
  #
  # Copy DelProf2 to other location as HiSPARC folders will be removed
  CreateDirectory $INSTDIR\DelProf2
  CopyFiles /SILENT $HisparcDir\admin\delprof2\*.exe $INSTDIR\DelProf2
  #
  # Stop the services
  DetailPrint "un.StopServices"
  ExecWait "$HisparcDir\persistent\startstopbatch\StopAdminMode.bat" $Result
  #
  # Uninstall the admin software
  DetailPrint "un.UninstallAdmin"
  ExecWait '"$HisparcDir\persistent\uninstallers\adminuninst.exe" /S' $Result
  # Uninstall the user software
  DetailPrint "un.UninstallUser"
  ExecWait '"$HisparcDir\persistent\uninstallers\useruninst.exe" /S' $Result
  # Remove Windows accounts
  DetailPrint "un.RemoveWindowsAccounts"
  ExecWait "net localgroup Administrators ${ADMHISPARC_USERNAME} /delete" $Result
  ExecWait "net user ${ADMHISPARC_USERNAME} /delete" $Result
  ExecWait "net user ${HISPARC_USERNAME} /delete" $Result
  # Remove AutoLogon feature
  DetailPrint "un.RemoveAutoLogon"
  DeleteRegValue HKLM "${AUTOLOGON_KEY}" ${ALV_USER_NAME}
  DeleteRegValue HKLM "${AUTOLOGON_KEY}" ${ALV_PASSWORD}
  DeleteRegValue HKLM "${AUTOLOGON_KEY}" ${ALV_AUTO_ADMIN}
  DeleteRegValue HKLM "${AUTOLOGON_KEY}" ${ALV_FORCE_ADMIN}
  DeleteRegValue HKLM "${AUTOLOGON_KEY}" ${ALV_DOMAIN_NAME}
  # Remove startmenu items
  SetShellVarContext all
  RMDir /r /REBOOTOK "$SMPROGRAMS\HiSPARC\Expert"
  RMDir /r /REBOOTOK "$SMPROGRAMS\HiSPARC\Status"
  RMDir /r /REBOOTOK "$SMPROGRAMS\HiSPARC"
  # Remove StartHiSPARC from Startup folder
  Delete /REBOOTOK "$SMSTARTUP\StartHiSPARCSoftware.lnk"
  # Remove the main uninstaller
  Delete "$HisparcDir\persistent\uninstallers\mainuninst.exe"
  # Give user last opportunity to copy data from HiSPARC directory structure
  MessageBox MB_ICONINFORMATION|MB_OK "Last chance to save data from HiSPARC folders; OK to continue and delete."
  # Remove (remainders of) both admhisparc and hisparc profiles and folders with Delprof2 utility
  ExecWait '"$INSTDIR\DelProf2\DelProf2.exe" /id:${ADMHISPARC_USERNAME} /q /i' $Result
  ExecWait '"$INSTDIR\DelProf2\DelProf2.exe" /id:${HISPARC_USERNAME} /q /i' $Result
  # Remove the HiSPARC folder (if still there).
  RMDir /r /REBOOTOK $HisparcDir
  # Remove the DelProf2 folder.
  RMDir /r /REBOOTOK $INSTDIR\DelProf2
  # Remove the hisparc user folder (if still there).
  SetOutPath $TEMP\$INSTDIR
  SetOutPath $TEMP
  RMDir /r /REBOOTOK $TEMP\Users\hisparc
  SetOutPath $INSTDIR
  # Remove HiSPARC key
  DeleteRegKey HKLM "${HISPARC_KEY}"
  DeleteRegKey HKLM "${HISPARC_UNINST_KEY}"
  SetAutoClose true
SectionEnd
