#
#   uninstaller.nsh ------
#   Create the admin uninstaller.
#

Function un.onInit
  DetailPrint "admin-un.onInit"
  
  InitPluginsDir
  # check if user has administrator rights
  xtInfoPlugin::IsAdministrator
  Pop $0
  ${If} $0 == "false"
    MessageBox MB_ICONEXCLAMATION "You have no administrator rights!$\nAdmin-Uninstallation aborted."
    Quit
  ${EndIf}
  
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" noReg
  StrCpy $AdminDir   "$HisparcDir\admin"
  ${DirState} $AdminDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $AdminDir does not exist!$\nAdmin-Uninstallation aborted."
    Quit
  ${Endif}
  DetailPrint "AdminDir: $AdminDir"
  Return
  
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nAdmin-Uninstallation aborted."
  Quit
FunctionEnd

#
# Remove OpenVPN
#
Section un.UninstOpenVPN
  DetailPrint "admin-un.UninstOpenVPN"
  # remove service
  ExecWait '"$AdminDir\openvpn\bin\openvpnserv.exe" -remove' $Result
  DetailPrint "VPN openvpnserv: $Result"
  # delete reg keys
  DeleteRegKey HKLM ${OPENVPN_KEY}
  # remove the tap devices
  ExecWait '"$AdminDir\openvpn\bin\tapinstall.exe" remove tap0901' $Result
  DetailPrint "VPN tapremove: $Result"
  # remove the folder
  RMDir /r /REBOOTOK "$AdminDir\openvpn"
SectionEnd

#
# Remove TightVNC.
#
Section un.UninstTightVNC
  DetailPrint "admin-un.UninstTightVNC"
  # remove service
  StrCpy $TvncFolder "$AdminDir\tightvnc"
  StrCpy $Program "$TvncFolder\${VNC_SERVICENAME}.exe"
  ExecWait '"$Program" -remove -silent' $Result
  DetailPrint "VNC tightvnc: $Result"
  # delete reg keys
  DeleteRegKey HKLM ${TIGHTVNCKEY}   
  # remove the folder
  RMDir /r /REBOOTOK "$AdminDir\tightvnc"
SectionEnd

#
# Remove nscp (NAGIOS)
#
Section un.UninstNscp
  DetailPrint "admin-un.UninstNscp"
  ExecWait '"$AdminDir\nsclientpp\NSClient++.exe" /stop' $Result
  DetailPrint "Nagios stop: $Result"
  ExecWait '"$AdminDir\nsclientpp\NSClient++.exe" /uninstall' $Result
  DetailPrint "Nagios uninstall: $Result"
  RMDir /r /REBOOTOK "$AdminDir\nsclientpp"
SectionEnd

#
# Remove ODBC
#
Section un.UninstODBC
  DetailPrint "admin-un.UninstODBC"
  DeleteRegKey   HKLM ${ODBCREGKEY}
  DeleteRegValue HKLM "${ODBCDSREGKEY}" "buffer"
  ExecWait '"$AdminDir\odbcconnector\Uninstall_HiSPARC.bat"' $Result
  DetailPrint "ODBC uninstall: $Result"
  RMDir /r /REBOOTOK "$AdminDir\odbcconnector"
SectionEnd

#
# Remove National Instruments Runtime Engine.
#
Section un.UninstNIRuntime
  DetailPrint "admin-un.UninstNIRuntime"
  MessageBox MB_YESNO|MB_ICONQUESTION "Do you also want to remove the NI Runtime Engine?" IDYES removeNI IDNO keepNI
removeNI:
  ReadRegStr $NIdir HKLM "${LABVIEW_KEY}" ${LABVIEW_DIR}
  ExecWait '"$NIdir\Shared\NIUninstaller\uninst.exe" /qb /x all' $Result
  DetailPrint "LabVIEW uninst: $Result"
  RMDir /r /REBOOTOK "$NIdir"
keepNI:
SectionEnd

#
# Remove the entire admin folder.
#
Section un.UninstProgs
  DetailPrint "admin-un.UninstProgs"
  # remove the entire admin folder
  RMDir /r /REBOOTOK "$AdminDir"
SectionEnd

#
# Stop and remove services from the service list.
#
Section un.UninstallServices
  DetailPrint "admin-un.UninstallServices"
  # stop the services
  SimpleSC::StopService ${VPN_SERVICENAME}
  SimpleSC::StopService ${VNC_SERVICENAME}
  SimpleSC::StopService ${NSCP_SERVICENAME}
  # remove the services
  SimpleSC::RemoveService ${VPN_SERVICENAME}
  SimpleSC::RemoveService ${VNC_SERVICENAME}
  SimpleSC::RemoveService ${NSCP_SERVICENAME}
SectionEnd

Section un.Uninstall
  DetailPrint "admin-un.Uninstall"
  Delete "$HisparcDir\persistent\uninstallers\adminuninst.exe"
  SetAutoClose true
SectionEnd
