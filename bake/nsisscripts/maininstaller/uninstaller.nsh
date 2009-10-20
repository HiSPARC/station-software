Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to reboot the system now?" IDYES Reboot IDNO NoReboot

  Reboot:
     ExecWait "shutdown -r -f -t 0"
  NoReboot:
FunctionEnd

Function un.onInit
  GetFullPathName $INSTDIR $INSTDIR\..\..\..
  #MessageBox MB_OK $INSTDIR
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES Remove IDNO Notremove
  Notremove:
     Abort
  Remove:
     ExecWait "$INSTDIR\hisparc\persistent\startstopbatch\StopAdminMode.bat"
FunctionEnd

#
# Uninstall the admin software
#
Section un.UninstallAdmin
  ExecWait "$INSTDIR\hisparc\persistent\uninstallers\adminuninst.exe /S"
SectionEnd

#
# Uninstall the admin software
#
Section un.UninstallUser
  ExecWait "$INSTDIR\hisparc\persistent\uninstallers\useruninst.exe /S"
SectionEnd

Section un.RemoveWindowsAccounts
    # admin
    ExecWait "net localgroup Administrators ${ADMHISPARC_USERNAME} /delete"
    ExecWait "net user ${ADMHISPARC_USERNAME} /delete"
    
    # user
    ExecWait "net user ${HISPARC_USERNAME} /delete"
SectionEnd

Section un.RemoveAutoLogon
    DeleteRegValue HKLM ${AUTOLOGONKEY} DefaultUserName
    DeleteRegValue HKLM ${AUTOLOGONKEY} DefaultPassword
    DeleteRegValue HKLM ${AUTOLOGONKEY} AutoAdminLogon
    DeleteRegValue HKLM ${AUTOLOGONKEY} ForceAdminLogon
    DeleteRegValue HKLM ${AUTOLOGONKEY} DefaultDomainName
SectionEnd

Section un.Uninstall
  Delete "$INSTDIR\hisparc\persistent\uninstallers\mainuninst.exe"
  
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to keep your persistent data?" IDYES Keep IDNO Remove

  Remove:
     #MessageBox MB_OK "Removing last part of the persistent directory"
     # delete the entire directory
     RmDir /r /REBOOTOK "$INSTDIR"
  Keep:

  #Remove startmenu items
  SetShellVarContext all
  RmDir /r /REBOOTOK "$SMPROGRAMS\HiSPARC"
  SetShellVarContext all
  #TODO: remove startup items as well
  Delete /REBOOTOK "$SMSTARTUP\StartHiSPARCSoftware.lnk"
  #TODO: Delete "$SMSTARTUP\..."
  
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd
