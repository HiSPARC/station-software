#
# Verwijder openvpn
#
Section un.UninstOpenVPN
    # stop service
    #SimpleSC::StopService "OpenVPN Service"
    ExecWait '"$InstallPathApplication\hisparc\admin\openvpn\bin\openvpnserv.exe" -remove'
    # delete reg keys
    DeleteRegKey HKLM "SOFTWARE\OpenVPN"

    # verwijder alle tap devices
    ExecWait '"$InstallPathApplication\hisparc\admin\openvpn\bin\tapinstall.exe" remove tap0901'
    # verwijder map
    RmDir /r /REBOOTOK "$InstallPathApplication\hisparc\admin\openvpn"
SectionEnd

#
# Remove tightvnc.
#
Section un.UninstTightVNC
    # stop service
    #SimpleSC::StopService "VNC Server"
	
	StrCpy $TvncFolder "$InstallPathApplication\hisparc\admin\tightvnc"
	StrCpy $Program "$TvncFolder\${VNC_SERVICENAME}.exe"
	ExecWait '"$Program" -remove'
  
	DeleteRegKey HKLM ${TIGHTVNCKEY}
    
    # remove folder
    RmDir /r /REBOOTOK "$InstallPathApplication\hisparc\admin\tightvnc"
SectionEnd

#
# verwijder nscp
#
Section un.UninstNscp
    ExecWait '"$InstallPathApplication\hisparc\admin\nsclientpp\NSClient++.exe" /stop'
    ExecWait '"$InstallPathApplication\hisparc\admin\nsclientpp\NSClient++.exe" /uninstall'

    RmDir /r /REBOOTOK "$InstallPathApplication\hisparc\admin\nsclientpp"
SectionEnd

#
# Verwijder ODBC
#
Section un.UninstODBC
    DeleteRegKey HKLM ${ODBCREGKEY}
    DeleteRegValue HKLM "${ODBCDSREGKEY}" "buffer"

    ExecWait '"$InstallPathApplication\hisparc\admin\odbcconnector\Uninstall_HiSPARC.bat"'
    
    #MessageBox MB_OK "Removing : $InstallPathApplication\hisparc\admin\odbcconnector"

    RmDir /r /REBOOTOK "$InstallPathApplication\hisparc\admin\odbcconnector"
SectionEnd

Section un.UninstNIRuntime
    MessageBox MB_YESNO|MB_ICONQUESTION "Wilt u National Instruments Runtime Environment ook verwijderen?" IDYES Remove IDNO Keep
    Remove:
       ExecWait "$NIDIR\Shared\NIUninstaller\uninst.exe /qb /x all"
       RmDir /r /REBOOTOK "$NIDIR"
    Keep:
SectionEnd

#
# Remove the entire admin folder.
#
Section un.UninstProgs
    # delete de hele map
    
    #MessageBox MB_OK "Removed: $InstallPathApplication\hisparc\admin"
    RmDir /r /REBOOTOK "$InstallPathApplication\hisparc\admin"
SectionEnd

Section un.UninstallServices
  SimpleSC::StopService ${VPNSERVICENAME}
  SimpleSC::StopService ${VNC_SERVICENAME}
  SimpleSC::StopService ${NSCPSERVICENAME}

  SimpleSC::RemoveService ${VPNSERVICENAME}
  SimpleSC::RemoveService ${VNC_SERVICENAME}
  SimpleSC::RemoveService ${NSCPSERVICENAME}
SectionEnd

#
# Deze functie wordt bij het opstarten van de uninstaller uitgevoerd.
#
Function un.onInit
  #MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  #Abort
FunctionEnd

Section un.Uninstall
  Delete "$InstallPathApplication\hisparc\persistent\uninstallers\adminuninst.exe"
  SetAutoClose true
SectionEnd
