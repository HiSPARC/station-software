#
#   uninstaller.nsh ------
#   Create the main uninstaller.
#   R.Hart@nikhef.nl, NIKHEF, Amsterdam
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
  StrCmp $HisparcDir "" nohomedir
  
  ${DirState} $HisparcDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "Folder $\"$HisparcDir$\" does not exist!$\nUninstallation canceled."
    Quit
  ${Endif}

  GetFullPathName $INSTDIR $INSTDIR\..\..\..
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES Remove IDNO Notremove
Notremove:
  Abort
Remove:
  ExecWait "$HisparcDir\persistent\startstopbatch\StopAdminMode.bat" $Result
  Return

nohomedir:
  MessageBox MB_ICONEXCLAMATION "Registry entry $\"${REG_PATH}$\" not set or defined!$\nUninstallation canceled."
  Quit
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to reboot the system now?" IDYES Reboot IDNO NoReboot

Reboot:
     ExecWait "shutdown -r -f -t 0"
NoReboot:
FunctionEnd

#
# Uninstall the admin software
#
Section un.UninstallAdmin
  DetailPrint "un.UninstallAdmin"
  ExecWait "$HisparcDir\persistent\uninstallers\adminuninst.exe /S" $Result
SectionEnd

#
# Uninstall the user software
#
Section un.UninstallUser
  DetailPrint "un.UninstallUser"
  ExecWait "$HisparcDir\persistent\uninstallers\useruninst.exe /S" $Result
SectionEnd

Section un.RemoveWindowsAccounts
  DetailPrint "un.RemoveWindowsAccounts"
  # admin
  ExecWait "net localgroup Administrators ${ADMHISPARC_USERNAME} /delete" $Result
  ExecWait "net user ${ADMHISPARC_USERNAME} /delete" $Result
  # user
  ExecWait "net user ${HISPARC_USERNAME} /delete" $Result
SectionEnd

Section un.RemoveAutoLogon
  DetailPrint "un.RemoveAutoLogon"
  DeleteRegValue HKLM ${AUTOLOGON_KEY} ${ALV_USER_NAME}
  DeleteRegValue HKLM ${AUTOLOGON_KEY} ${ALV_PASSWORD}
  DeleteRegValue HKLM ${AUTOLOGON_KEY} ${ALV_AUTO_ADMIN}
  DeleteRegValue HKLM ${AUTOLOGON_KEY} ${ALV_FORCE_ADMIN}
  DeleteRegValue HKLM ${AUTOLOGON_KEY} ${ALV_DOMAIN_NAME}
SectionEnd

Section un.RemoveHiSPARCkey
  DetailPrint "un.RemoveHiSPARCkey"
  DeleteRegKey HKLM "${HISPARC_KEY}"
  DeleteRegKey HKLM "${HISPARC_UNINST_KEY}"
SectionEnd

Section un.Uninstall
  DetailPrint "un.Uninstall"
  
  # Remove startmenu items
  SetShellVarContext all
  RMDir /r /REBOOTOK "$SMPROGRAMS\HiSPARC\Expert"
  RMDir /r /REBOOTOK "$SMPROGRAMS\HiSPARC\Status"
  RMDir /r /REBOOTOK "$SMPROGRAMS\HiSPARC"
  # Remove StartHiSPARC from Startup folder
  Delete /REBOOTOK "$SMSTARTUP\StartHiSPARCSoftware.lnk"
  # Remove the main uninstaller
  Delete "$HisparcDir\persistent\uninstallers\mainuninst.exe"
  
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to keep the HiSPARC program folder?" IDYES Keep IDNO Remove
Remove:
  RMDir /r /REBOOTOK $HisparcDir
Keep:
  SetAutoClose true
SectionEnd
