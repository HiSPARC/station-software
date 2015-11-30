#
#   install.nsh ------
#   Admin installer.
#   Jan 2013: multiple (2) NI-RunTimeEngines
#   May 2013: - separate OpenVpn folder for 32-bit and 64-bit
#             - popup-window in case of error
#   Aug 2013: - 64-bit: only OpenVPN and TightVNC have a true 64-bit executable
#               Other application still use the 32-bit registry.
#               OpenVPN, due to a bug in version 2.2.2, as well.
#   Oct 2015: - only 1 LabView RTE, version 2014 (RH)
#   Nov 2015: - NI-RTE 2014: installation fails sometimes with error 1603 (x643),
#               but installation seems ok. Error will be ignored.
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
  
  StrCpy $FileName "$OpenVpnDir\bin\tapinstall.exe"
  Call fileExists
  StrCpy $FileName "$OpenVpnDir\bin\openvpnserv.exe"
  Call fileExists
  StrCpy $FileName "$TvncFolder\${VNC_SERVICENAME}.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\nsclientpp\NSClient++.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\odbcconnector\Install_HiSPARC.bat"
  Call fileExists
  StrCpy $FileName "$AdminDir\nirte2014\setup.exe"
  Call fileExists
  StrCpy $FileName "$AdminDir\ftdi_drivers\dpinst.exe"
  Call fileExists
SectionEnd

#
# Install OpenVPN.
#
Section -OpenVPNSetup
  DetailPrint "admin-OpenVPNSetup"
  # OpenVPN 2.2.2 64-bit version, still reads its registry as a 32-bit application
  SetRegView 32
  # register
  WriteRegStr HKLM ${OPENVPN_KEY} ""         "$AdminDir"
  WriteRegStr HKLM ${OPENVPN_KEY} config_dir "$OpenVpnDir\config"
  WriteRegStr HKLM ${OPENVPN_KEY} config_ext "ovpn"
  WriteRegStr HKLM ${OPENVPN_KEY} exe_path   "$OpenVpnDir\bin\openvpn.exe"
  WriteRegStr HKLM ${OPENVPN_KEY} log_append "0"
  WriteRegStr HKLM ${OPENVPN_KEY} log_dir    "$OpenVpnDir\log"
  WriteRegStr HKLM ${OPENVPN_KEY} priority   "NORMAL_PRIORITY_CLASS"
  # install tap driver
  ExecWait '"$OpenVpnDir\bin\tapinstall.exe" install "$OpenVpnDir\driver\OemWin2k.inf" tap0901' $Result
  StrCpy $Message "VPN tapinstall: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "ERROR: $Message"
  ${Endif}
  # service
  ExecWait '"$OpenVpnDir\bin\openvpnserv.exe" -install' $Result
  StrCpy $Message "VPN openvpnserv: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "ERROR: $Message"
  ${Endif}
  # unzip certificate zip
  nsisunz::UnzipToLog "$CertZip" "$OpenVpnDir\config"
  ${If} $Architecture == "64"
    SetRegView 64
  ${Endif}
SectionEnd

#
# Install TightVNC.
#
Section -TightVNCSetup
  DetailPrint "admin-TightVNCSetup"
  # register
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
  StrCpy $Message "VNC tightvnc: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "ERROR: $Message"
  ${Endif}
SectionEnd

#
# Install nsclient++ (NAGIOS)
#
Section -NscpSetup
  DetailPrint "admin-NscpSetup"
  ExecWait '"$AdminDir\nsclientpp\NSClient++.exe" /install' $Result
  StrCpy $Message "Nagios NSClient++: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "ERROR: $Message"
  ${Endif}
SectionEnd

#
# Install ODBC.
#
Section -ODBCSetup
  DetailPrint "admin-ODBCSetup"
  SetRegView 32
  # install
  ExecWait '"$AdminDir\odbcconnector\Install_HiSPARC.bat"' $Result
  StrCpy $Message "ODBC install: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "ERROR: $Message"
  ${Endif}
  # register
  WriteRegStr HKLM ${ODBCREGKEY}     DATABASE    "buffer"
  WriteRegStr HKLM ${ODBCREGKEY}     DESCRIPTION "HiSPARC buffer"
  WriteRegStr HKLM ${ODBCREGKEY}     Driver      '${ODBCDRVPATH}'
  WriteRegStr HKLM ${ODBCREGKEY}     PORT        3306
  WriteRegStr HKLM ${ODBCREGKEY}     PWD         '${BUFFERPASS}'
  WriteRegStr HKLM ${ODBCREGKEY}     SERVER      "${BDBHOST}"
  WriteRegStr HKLM ${ODBCREGKEY}     UID         "buffer"
  WriteRegStr HKLM '${ODBCDSREGKEY}' buffer      '${ODBCDRV}'
  ${If} $Architecture == "64"
    SetRegView 64
  ${Endif}
SectionEnd

#
# Install LabVIEW Run-Time-Engine
# ONE version is installed: 2014
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
#
Section -LabviewRuntimeSetup
  DetailPrint "admin-LabviewRuntimeSetup"
  SetRegView 32
  ExecWait '"$AdminDir\nirte2014\setup.exe" /AcceptLicenses yes /r:n /q' $Result
  StrCpy $Message "LabVIEW RTE 2014 setup: $Result"
  DetailPrint $Message
  ${If} $Result != 3010
  ${AndIf} $Result != 0
  ${Andif} $Result != 1603
    MessageBox MB_ICONEXCLAMATION "ERROR: $Message"
  ${Endif}
  ${If} $Architecture == "64"
    SetRegView 64
  ${Endif}
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
