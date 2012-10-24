#
#   uninstaller.nsh ------
#   Create the main uninstaller.
#   R.Hart@nikhef.nl, Nikhef, Amsterdam
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
  # Stop the services
  DetailPrint "un.StopServices"
  ExecWait "$HisparcDir\persistent\startstopbatch\StopAdminMode.bat" $Result
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
  # Keep the HiSPARC folder or not.
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to keep the HiSPARC program folder?" IDYES keepFolder IDNO removeFolder
removeFolder:
  RMDir /r /REBOOTOK $HisparcDir
keepFolder:
  # Remove HiSPARC key
  DeleteRegKey HKLM "${HISPARC_KEY}"
  DeleteRegKey HKLM "${HISPARC_UNINST_KEY}"
  SetAutoClose true
SectionEnd
