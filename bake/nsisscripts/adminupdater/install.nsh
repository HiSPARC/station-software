#
# Install openvpn.
#
Section -OpenVPNSetup
    # register
    WriteRegStr HKLM "SOFTWARE\OpenVPN" "" "$InstallPathApplication\hisparc\admin"
    WriteRegStr HKLM "SOFTWARE\OpenVPN" config_dir "$InstallPathApplication\hisparc\admin\OpenVPN\config"
    WriteRegStr HKLM "SOFTWARE\OpenVPN" config_ext "ovpn"
    WriteRegStr HKLM "SOFTWARE\OpenVPN" exe_path "$InstallPathApplication\hisparc\admin\OpenVPN\bin\openvpn.exe"
    WriteRegStr HKLM "SOFTWARE\OpenVPN" log_append "0"
    WriteRegStr HKLM "SOFTWARE\OpenVPN" log_dir "$InstallPathApplication\hisparc\admin\OpenVPN\log"
    WriteRegStr HKLM "SOFTWARE\OpenVPN" priority "NORMAL_PRIORITY_CLASS"

    # installeer tap driver
    ExecWait '"$InstallPathApplication\hisparc\admin\openvpn\bin\tapinstall.exe" install "$InstallPathApplication\hisparc\admin\openvpn\driver\oemWin2k.inf" tap0901'

    # service
    ExecWait '"$InstallPathApplication\hisparc\admin\openvpn\bin\openvpnserv.exe" -install'
SectionEnd

#
# login gegevens.
#
Section -LoginGegevens
    # unzip certificaat zip
    nsisunz::UnzipToLog "$CertZip" "${InstallationDirectory}\openvpn\config"
SectionEnd

#
# Install tightvnc.
#
Section -TightVNCSetup
    # register
	StrCpy $TvncFolder "$InstallPathApplication\hisparc\admin\tightvnc"
  
	WriteRegStr   HKLM ${TIGHTVNCKEY}         Path                      "$TvncFolder"
	WriteRegStr   HKLM ${TIGHTVNCKEY}         StartMenuGroup            "TightVNC"
	WriteRegDWORD HKLM ${TVNCCOMPONENTSKEY}   "TightVNC Server"         1
	WriteRegDWORD HKLM ${TVNCCOMPONENTSKEY}   "TightVNC Viewer"         1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       AcceptHttpConnections     1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       AcceptRfbConnections      1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       AllowLoopback             0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       AlwaysShared              0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       BlankScreen               0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       BlockLocalInput           0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       BlockRemoteInput          0 
	WriteRegBin   HKLM ${TVNCSERVERKEY}       ControlPassword           ${VNC_PASSWORD}
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       DisconnectAction          0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       DisconnectClients         1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       EnableFileTransfers       1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       EnableUrlParams           1
	WriteRegStr   HKLM ${TVNCSERVERKEY}       ExtraPorts                "" 
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       GrabTransparentWindows    1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       HttpPort                  5800
	WriteRegStr   HKLM ${TVNCSERVERKEY}       IpAccessControl           ""
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       LocalInputPriority        0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       LocalInputPriorityTimeout 3
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       LogLevel                  0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       LoopbackOnly              0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       NeverShared               0
	WriteRegBin   HKLM ${TVNCSERVERKEY}       Password                  ${VNC_PASSWORD} 
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       PollingInterval           1000
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       QueryAcceptOnTimeout      0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       QueryTimeout              30
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       RemoveWallpaper           1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       RfbPort                   5900
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       RunControlInterface       1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       SaveLogToAllUsersPath     0
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       UseControlAuthentication  1
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       UseVncAuthentication      1
	WriteRegStr   HKLM ${TVNCSERVERKEY}       VideoClasses              ""
	WriteRegDWORD HKLM ${TVNCSERVERKEY}       VideoRecognitionInterval  3000
    
    # service
	StrCpy $Program "$TvncFolder\${VNC_SERVICENAME}.exe"
	ExecWait '"$Program" -install'

    #DetailPrint "TightVNC service installed."
SectionEnd

#
# installeer nsclient++
#
Section -NscpSetup
    ExecWait '"$InstallPathApplication\hisparc\admin\nsclientpp\NSClient++.exe" /install'
SectionEnd

#
# Installeer ODBC.
#
Section -ODBCSetup
    ExecWait '"$InstallPathApplication\hisparc\admin\odbcconnector\Install_HiSPARC.bat"'

    WriteRegStr HKLM ${ODBCREGKEY} DATABASE    "buffer"
    WriteRegStr HKLM ${ODBCREGKEY} DESCRIPTION "HiSPARC buffer"
    WriteRegStr HKLM ${ODBCREGKEY} Driver      '${ODBCDRVPATH}'
    WriteRegStr HKLM ${ODBCREGKEY} PORT        3306
    WriteRegStr HKLM ${ODBCREGKEY} PWD         '${BUFFERPASS}'
    WriteRegStr HKLM ${ODBCREGKEY} SERVER      "${BDBHOST}"
    WriteRegStr HKLM ${ODBCREGKEY} UID         "buffer"

    WriteRegStr HKLM '${ODBCDSREGKEY}' buffer '${ODBCDRV}'
SectionEnd

Section -LabviewRuntimeSetup
  ExecWait "$InstallPathApplication\hisparc\admin\niruntimeinstaller\setup.exe hisparcspec.ini /acceptlicenses yes /r:n /q"
SectionEnd

#
# Install FTDI USB drivers
#
Section -FTDIDrivers
    ExecWait "$InstallPathApplication\hisparc\admin\ftdi_drivers\dpinst.exe /q"
SectionEnd

#
# Post install page die de services start.
#
Section RegisterServices
    # zet de vpn service op automatisch en start de service.
    SimpleSC::SetServiceStartType ${VPNSERVICENAME} 2
    SimpleSC::StartService ${VPNSERVICENAME}
    SimpleSC::GetErrorMessage

    # zet de vnc service op automatisch en start de service.
    SimpleSC::SetServiceStartType ${VNC_SERVICENAME} 2
    SimpleSC::StartService ${VNC_SERVICENAME}
    SimpleSC::GetErrorMessage

    # zet de nscp service op automatisch en start de service.
    SimpleSC::SetServiceStartType ${NSCPSERVICENAME} 2
    SimpleSC::StartService ${NSCPSERVICENAME}
    SimpleSC::GetErrorMessage
SectionEnd