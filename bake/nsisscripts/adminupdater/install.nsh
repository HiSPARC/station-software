#
#   install.nsh ------
#   Admin installer.
#

#
# Check existance of executables.
# On error, exit.
#
Section -CheckExecutables
  DetailPrint "admin-CheckExecutables"
  
  ${DirState} $AdminDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $AdminDir does not exist!$\nAdmin-Installation aborted."
    Quit
  ${Endif}
  
  StrCpy $FileName "$AdminDir\openvpn\bin\tapinstall.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\openvpn\bin\openvpnserv.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\tightvnc\${VNC_SERVICENAME}.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\nsclientpp\NSClient++.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\odbcconnector\Install_HiSPARC.bat"
  Call fileExists
  StrCpy $FileName "$AdminDir\niruntimeinstaller\setup.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\ftdi_drivers\dpinst.exe"
  Call fileExists
SectionEnd

#
# Install OpenVPN.
#
Section -OpenVPNSetup
  DetailPrint "admin-OpenVPNSetup"
  # register
  WriteRegStr HKLM ${OPENVPN_KEY} ""         "$AdminDir"
  WriteRegStr HKLM ${OPENVPN_KEY} config_dir "$AdminDir\OpenVPN\config"
  WriteRegStr HKLM ${OPENVPN_KEY} config_ext "ovpn"
  WriteRegStr HKLM ${OPENVPN_KEY} exe_path   "$AdminDir\OpenVPN\bin\openvpn.exe"
  WriteRegStr HKLM ${OPENVPN_KEY} log_append "0"
  WriteRegStr HKLM ${OPENVPN_KEY} log_dir    "$AdminDir\OpenVPN\log"
  WriteRegStr HKLM ${OPENVPN_KEY} priority   "NORMAL_PRIORITY_CLASS"
  # install tap driver
  ExecWait '"$AdminDir\openvpn\bin\tapinstall.exe" install "$AdminDir\openvpn\driver\oemWin2k.inf" tap0901' $Result
  DetailPrint "VPN tapinstall: $Result"
  # service
  ExecWait '"$AdminDir\openvpn\bin\openvpnserv.exe" -install' $Result
  DetailPrint "VPN openvpnserv: $Result"
  # unzip certificate zip
  nsisunz::UnzipToLog "$CertZip" "$AdminDir\openvpn\config"
SectionEnd

#
# Install TightVNC.
#
Section -TightVNCSetup
  DetailPrint "admin-TightVNCSetup"
  # register
  StrCpy $TvncFolder "$AdminDir\tightvnc"
  WriteRegStr   HKLM ${TIGHTVNC_KEY}         Path                      "$TvncFolder"
  WriteRegStr   HKLM ${TIGHTVNC_KEY}         StartMenuGroup            "TightVNC"
  WriteRegDWORD HKLM ${TVNCCOMPONENTS_KEY}   "TightVNC Server"         1
  WriteRegDWORD HKLM ${TVNCCOMPONENTS_KEY}   "TightVNC Viewer"         1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AcceptHttpConnections     1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AcceptRfbConnections      1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AllowLoopback             0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AlwaysShared              0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       BlankScreen               0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       BlockLocalInput           0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       BlockRemoteInput          0 
  WriteRegBin   HKLM ${TVNCSERVER_KEY}       ControlPassword           ${VNC_CTRL_PASSWORD}
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       DisconnectAction          0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       DisconnectClients         1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       EnableFileTransfers       1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       EnableUrlParams           1
  WriteRegStr   HKLM ${TVNCSERVER_KEY}       ExtraPorts                "" 
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       GrabTransparentWindows    1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       HttpPort                  5800
  WriteRegStr   HKLM ${TVNCSERVER_KEY}       IpAccessControl           ""
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LocalInputPriority        0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LocalInputPriorityTimeout 3
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LogLevel                  0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LoopbackOnly              0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       NeverShared               0
  WriteRegBin   HKLM ${TVNCSERVER_KEY}       Password                  ${VNC_PASSWORD} 
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       PollingInterval           1000
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       QueryAcceptOnTimeout      0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       QueryTimeout              30
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       RemoveWallpaper           1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       RfbPort                   5900
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       RunControlInterface       1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       SaveLogToAllUsersPath     0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       UseControlAuthentication  1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       UseVncAuthentication      1
  WriteRegStr   HKLM ${TVNCSERVER_KEY}       VideoClasses              ""
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       VideoRecognitionInterval  3000
  # service
  StrCpy $Program "$TvncFolder\${VNC_SERVICENAME}.exe"
  ExecWait '"$Program" -install -silent' $Result
  DetailPrint "VNC tightvnc: $Result"
SectionEnd

#
# Install nsclient++ (NAGIOS)
#
Section -NscpSetup
  DetailPrint "admin-NscpSetup"
  ExecWait '"$AdminDir\nsclientpp\NSClient++.exe" /install' $Result
  DetailPrint "Nagios NSClient++: $Result"
SectionEnd

#
# Install ODBC.
#
Section -ODBCSetup
  DetailPrint "admin-ODBCSetup"
  # install
  ExecWait '"$AdminDir\odbcconnector\Install_HiSPARC.bat"' $Result
  DetailPrint "ODBC install: $Result"
  # register
  WriteRegStr HKLM ${ODBCREGKEY}     DATABASE    "buffer"
  WriteRegStr HKLM ${ODBCREGKEY}     DESCRIPTION "HiSPARC buffer"
  WriteRegStr HKLM ${ODBCREGKEY}     Driver      '${ODBCDRVPATH}'
  WriteRegStr HKLM ${ODBCREGKEY}     PORT        3306
  WriteRegStr HKLM ${ODBCREGKEY}     PWD         '${BUFFERPASS}'
  WriteRegStr HKLM ${ODBCREGKEY}     SERVER      "${BDBHOST}"
  WriteRegStr HKLM ${ODBCREGKEY}     UID         "buffer"
  WriteRegStr HKLM '${ODBCDSREGKEY}' buffer      '${ODBCDRV}'
SectionEnd

#
# Install LabVIEW
#
Section -LabviewRuntimeSetup
  DetailPrint "admin-LabviewRuntimeSetup"
  ExecWait '"$AdminDir\niruntimeinstaller\setup.exe" hisparcspec.ini /AcceptLicenses yes /r:n /q' $Result
  DetailPrint "LabVIEW setup: $Result"
SectionEnd

#
# Install FTDI USB drivers
#
Section -FTDIDrivers
  DetailPrint "admin-FTDIDrivers"
  ExecWait '"$AdminDir\ftdi_drivers\dpinst.exe" /q' $Result
  DetailPrint "FTDI dpinst: $Result"
SectionEnd

#
# Post install page. Stratup the services
#
Section -RegisterServices
  DetailPrint "admin-RegisterServices"
  # Put the OpenVPN service to automatic and start it.
  SimpleSC::SetServiceStartType ${VPN_SERVICENAME} 2
  SimpleSC::StartService        ${VPN_SERVICENAME}
  SimpleSC::GetErrorMessage
  # Put the TightVNC service to automatic and start it.
  SimpleSC::SetServiceStartType ${VNC_SERVICENAME} 2
  SimpleSC::StartService        ${VNC_SERVICENAME}
  SimpleSC::GetErrorMessage
  # Put the nscp service to automatic and start it.
  SimpleSC::SetServiceStartType ${NSCP_SERVICENAME} 2
  SimpleSC::StartService        ${NSCP_SERVICENAME}
  SimpleSC::GetErrorMessage
SectionEnd
