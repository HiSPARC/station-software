#########################################################################################
#
# HiSPARC NSIS admin installer
# Code to install individual services
# Called from:  - ././bakescripts/bake.py
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this installer does:
# - Install individual services
#
#########################################################################################
#
# Jan 2013: - Multiple (2) NI-RunTimeEngines                                (x32)
# May 2013: - Separate OpenVPN folder for 32-bit and 64-bit
#           - Popup-window in case of error
#           - 64-bit: TightVNC has now a true 64-bit executable
# Aug 2013: - 64-bit OpenVPN, due to a bug in version 2.2.2, remains
#             the 32 bits version
#           - Some applications still use the 32-bit registry
#           - NSClient++ version 0.3.7                                      (x32)
#           - ODBC version 5.1                                              (x32)
# Oct 2015: - Only 1 LabView RTE, version 2014                              (x32)
# Nov 2015: - NI-RTE 2014: installation fails sometimes with error 1603
#             but installation seems ok. Error will be ignored
# Aug 2016: - NI-RTE 2015 (x32) and check on folder
#             C:\Users\Public\Documents
#           - Disable FTDI COM port enumeration
# Jul 2017: - OpenVPN version 2.4.3                                         (x32 and x64)
#           - OpenVPN now requires .NET 4.0 full version                    (x32 and x64)
#           - TAP version 9.0.0.21                                          (x32 and x64)
#           - TightVNC version 2.8.8.0                                      (x32 and x64)
#           - NI-RTE 2016                                                   (x32)
#           - FTDI drivers version 2.12.26                                  (x32 and x64)
#           - Delprof2 version 1.6.0                                        (x32 and x64)
#           - Introduce uniform naming convention service directories
# Oct 2017: - Prolific PL2303 Serial-to-USB driver 3.8.12.0                 (x32 and x64)
#           - SiLabs CP210X USB driver 6.7.4                                (x32 and x64)
#           - NI-RTE 2017 (a dedicated installer in LabView is created)     (x32)
# Apr 2018  - OpenVPN version 2.4.5                                         (x32 and x64)
#           - TAP version 9.21.2                                            (x32 and x64)
#           - NSClient++ version 0.5.2.35 (.msi)                            (x32 and x64)
#           - NI-RTE 2017SP1 (a dedicated installer in LabView is created)  (x32)
#           - FTDI drivers version 2.12.28                                  (x32 and x64)
#           - Prolific PL2303 Serial-to-USB driver 3.8.18.0                 (x32 and x64)
#           - SiLabs CP210X USB driver 6.8.0.1951                           (x32 and x64)
#           - IVI-Foundation removal tool version 5.8.0 for NI-Visa         (x32)
#           - Check every 60 seconds whether the OpenVPN, TightVNC and
#             NSClient++ services are running. If not try to restart
#             This procedure continues for 15 mins, then a pc-reboot is
#             initiated.
# Aug 2018  - OpenVPN version 2.4.6                                         (x32 and x64)
#           - TightVNC version 2.8.11.0                                     (x32 and x64)
# Feb 2019: - Python 2.7.15                                                 (x32)
# Mar 2019: - 'HiSPARCStatus' added as Scheduled Task in Windows 10
#           - Prolific PL2303 Serial-to-USB driver 3.8.25.0                 (x32 and x64)
#
#########################################################################################

Section -InstallServices
#
# Get admin installation directory
  DetailPrint "admin-InstallServices"
# Check whether admin directory exists
  ${DirState} $AdminDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $AdminDir does not exist!$\nAdmin-Installer aborted."
    Quit
  ${Endif}
# Check if following services exist:
# OpenVPN
  StrCpy $FileName "$OpenVPNDir\bin\${TAP_EXENAME}.exe"
  Call fileExists
  StrCpy $FileName "$OpenVPNDir\bin\${VPN_EXENAME}.exe"
  Call fileExists
# TightVNC
  StrCpy $FileName "$TightVNCDir\${VNC_EXENAME}.exe"
  Call fileExists
# Nagios Client++
  StrCpy $FileName "$NSCPDir\${NSCP_EXENAME}.msi"
  Call fileExists
# ODBC database connector
  StrCpy $FileName "$ODBCDir\${INSTALL_BAT}.bat"
  Call fileExists
# Visual studio redistribution for ODBC
  StrCpy $FileName "$ODBCDir\${VCRE32_EXENAME}.exe"
  Call fileExists
  StrCpy $FileName "$ODBCDir\${VCRE64_EXENAME}.exe"
  Call fileExists
# National Instruments Run Time Engine
  StrCpy $FileName "$NIRTEDir\${NIRTE_EXENAME}.exe"
  Call fileExists
# IVI-Foundation removal tool for NI-Visa
  StrCpy $FileName "$NIRTEDir\${VISA_EXENAME}.exe"
  Call fileExists
# FTDI USB drivers
  StrCpy $FileName "$FTDIDir\${FTDI_EXENAME}.exe"
  Call fileExists
# DelProf2 profile removal tool
  StrCpy $FileName "$DelProfDir\${DELPROF_EXENAME}.exe"
  Call fileExists
# Prolific PL2303 driver
  StrCpy $FileName "$PL2303Dir\${PL2303_EXENAME}.exe"
  Call fileExists
# SiLabs CP210X driver
  StrCpy $FileName "$CP210XDir\${CP210X_EXENAME}.exe"
  Call fileExists
# Schedule Task1
  StrCpy $FileName "$TASKDir\${TASK1_CREATE}.bat"
  Call fileExists
SectionEnd

Section -OpenVPNSetup
#
# Install OpenVPN and TAP-Windows virtual ethernet driver
  DetailPrint "admin-OpenVPNSetup"
# Check if .NET 4.0 is installed for OpenVPN (required as of version 2.4.2)
  ReadRegDWORD $R0 HKLM "${NET_KEY}" Install
# If not; install 
  ${If} $R0 != 1
    ExecWait '"$AdminDir\openvpn\${NETInstaller}" /q' $Result
    Sleep 3000
    StrCpy $Message "Microsoft .NET Framework v${NETVersion} Setup: $Result"
    DetailPrint $Message
    ${If} $Result != 0
      MessageBox MB_ICONEXCLAMATION "Microsoft .NET Framework v${NETVersion} Setup ERROR: $Message"
    ${Endif}
  ${Else}
    DetailPrint "Microsoft .NET Framework v${NETVersion} is already installed!"
  ${Endif}
# Write OpenVPN registry keys
  WriteRegStr HKLM ${OPENVPN_KEY} ""               "$AdminDir"
  WriteRegStr HKLM ${OPENVPN_KEY} config_dir       "$OpenVPNDir\config"
  WriteRegStr HKLM ${OPENVPN_KEY} config_ext       "ovpn"
  WriteRegStr HKLM ${OPENVPN_KEY} exe_path         "$OpenVPNDir\bin\openvpn.exe"
  WriteRegStr HKLM ${OPENVPN_KEY} log_dir          "$OpenVPNDir\log"
  WriteRegStr HKLM ${OPENVPN_KEY} log_append       "0"
  WriteRegStr HKLM ${OPENVPN_KEY} ovpn_admin_group "OpenVPN Administrators"
  WriteRegStr HKLM ${OPENVPN_KEY} priority         "NORMAL_PRIORITY_CLASS"
# Install TAP-Windows virtual ethernet driver
  ExecWait '"$OpenVPNDir\bin\${TAP_EXENAME}.exe" install "$OpenVPNDir\driver\OemVista.inf" ${TAP} /S' $Result
  Sleep 3000
  StrCpy $Message "Install TAP-Windows Virtual Ethernet Driver: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "TAP-Windows ERROR: $Message"
  ${Endif}
# Install OpenVPN service
  ExecWait '"$OpenVPNDir\bin\openvpnserv2.exe" -install' $Result
  Sleep 3000
  StrCpy $Message "Install OpenVPNserv2: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "OpenVPN ERROR: $Message"
  ${Endif}
# Unzip certificate.zip
  nsisunz::UnzipToLog "$CertZip" "$OpenVPNDir\config"
SectionEnd

Section -TightVNCSetup
#
# Install TightVNC
  DetailPrint "admin-TightVNCSetup"
# Write TightVNC registry keys
  WriteRegStr   HKLM ${TIGHTVNC_KEY}         Path                        "$TightVNCDir"
  WriteRegStr   HKLM ${TIGHTVNC_KEY}         StartMenuGroup              "TightVNC"
  WriteRegDWORD HKLM ${TVNCCOMPONENTS_KEY}   "TightVNC Server"           1
  WriteRegDWORD HKLM ${TVNCCOMPONENTS_KEY}   "TightVNC Viewer"           1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AcceptHttpConnections       1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AcceptRfbConnections        1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AllowLoopback               0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       AlwaysShared                0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       BlankScreen                 0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       BlockLocalInput             0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       BlockRemoteInput            0 
  WriteRegBin   HKLM ${TVNCSERVER_KEY}       ControlPassword             ${VNC_CTRL_PASSWORD}
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       DisconnectAction            0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       DisconnectClients           1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       EnableFileTransfers         1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       EnableUrlParams             1
  WriteRegStr   HKLM ${TVNCSERVER_KEY}       ExtraPorts                  "" 
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       GrabTransparentWindows      1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       HttpPort                    5800
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       IdleTimeout                 0
  WriteRegStr   HKLM ${TVNCSERVER_KEY}       IpAccessControl             ""
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LocalInputPriority          0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LocalInputPriorityTimeout   3
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LogLevel                    0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       LoopbackOnly                0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       NeverShared                 0
  WriteRegBin   HKLM ${TVNCSERVER_KEY}       Password                    ${VNC_PASSWORD} 
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       PollingInterval             1000
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       QueryAcceptOnTimeout        0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       QueryTimeout                30
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       RemoveWallpaper             1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       RepeatControlAuthentication 1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       RfbPort                     5900
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       RunControlInterface         1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       SaveLogToAllUsersPath       0
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       UseControlAuthentication    1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       UseMirrorDriver             1
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       UseVncAuthentication        1
  WriteRegStr   HKLM ${TVNCSERVER_KEY}       VideoClasses                ""
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       VideoRecognitionInterval    3000
  WriteRegDWORD HKLM ${TVNCSERVER_KEY}       VideoRects                  ""
# Install TightVNC service
  ExecWait '"$TightVNCDir\${VNC_EXENAME}.exe" -install -silent' $Result
  Sleep 3000
  StrCpy $Message "Install TightVNC server: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "TightVNC ERROR: $Message"
  ${Endif}
SectionEnd

Section -NSCPSetup
#
# Install Nagios Client++
  DetailPrint "admin-NSCPSetup"
# Check if Nagios Client++ .ini file exists:
  StrCpy $FileName "$NSCPDir\${NSCP_ININAME}.txt"
  Call fileExists
# Following line solves the problem of having spaces in path names in arguments for .msi
# This may not be save for future Windows versions as the 'short' path-name is used...
  GetFullPathName /SHORT $0 "$NSCPDir"
# Install service
  ExecWait 'msiexec.exe /i "$NSCPDir\${NSCP_EXENAME}.msi" INSTALLLOCATION="$0\" /q' $Result
  Sleep 3000
  StrCpy $Message "Install Nagios Client++: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "Nagios Client++ ERROR: $Message"
  ${Endif}
# Overwrite nsclient.ini with file containing proper nscp settings...
# This is required as user provided .ini is overwritten by the .msi installer 
  Delete "$NSCPDir\${NSCP_ININAME}.ini"
  Rename "$NSCPDir\${NSCP_ININAME}.txt" "$NSCPDir\${NSCP_ININAME}.ini"
SectionEnd

Section -ODBCSetup
#
# Install ODBC
  DetailPrint "admin-ODBCSetup"
# Install Visual C++ Redistributable Packages for Visual Studio 2013 (x32)
# (msvcr120.dll required)
  ExecWait '"$ODBCDir\${VCRE32_EXENAME}.exe" /q' $Result
  Sleep 3000
  StrCpy $Message "Install Visual Studio 2013 x32: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "Visual Studio 2013 x32 ERROR: $Message"
  ${Endif}
  ${If} $Architecture == "64"
# Install Visual C++ Redistributable Packages for Visual Studio 2013 (x64) as well
# (msvcr120.dll required)
    ExecWait '"$ODBCDir\${VCRE64_EXENAME}.exe" /q' $Result
    Sleep 3000
    StrCpy $Message "Install Visual Studio 2013 x64: $Result"
    DetailPrint $Message
    ${If} $Result != 0
      MessageBox MB_ICONEXCLAMATION "Visual Studio 2013 x64 ERROR: $Message"
    ${Endif}
  ${Endif}
# x32 only!
  SetRegView 32
# Install service
  ExecWait '"$ODBCDir\${INSTALL_BAT}.bat"' $Result
  Sleep 3000
  StrCpy $Message "Install ODBC: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "ODBC ERROR: $Message"
  ${Endif}
# Register keys
  WriteRegStr HKLM ${ODBC_KEY}     DATABASE    "buffer"
  WriteRegStr HKLM ${ODBC_KEY}     DESCRIPTION "HiSPARC buffer"
  WriteRegStr HKLM ${ODBC_KEY}     Driver      '${ODBCDRVPATH}'
  WriteRegStr HKLM ${ODBC_KEY}     PORT        3306
  WriteRegStr HKLM ${ODBC_KEY}     PWD         '${BUFFERPASS}'
  WriteRegStr HKLM ${ODBC_KEY}     SERVER      "${BDBHOST}"
  WriteRegStr HKLM ${ODBC_KEY}     UID         "buffer"
  WriteRegStr HKLM '${ODBCDS_KEY}' buffer      '${ODBCDRV}'
  ${If} $Architecture == "64"
    SetRegView 64
  ${Endif}
SectionEnd

Section -NIRTESetup
#
# Install National Instruments (LabVIEW) Run-Time-Engine
  DetailPrint "admin-NIRTESetup"
# x32 only!
  SetRegView 32
# C:\Users\Public\Documents exists?
  StrCpy $FolderName "C:\Users\Public\Documents"
  ${DirState} $FolderName $Result
  ${If} $Result < 0
# If C:\Users\Public\Documents does not exist, create it
    CreateDirectory $FolderName
  ${EndIf}
# Install service
  ExecWait '"$NIRTEDir\${NIRTE_EXENAME}.exe" /AcceptLicenses yes /r:n /q' $Result
  Sleep 3000
  StrCpy $Message "Install National Instruments RTE: $Result"
  DetailPrint $Message
# NB: Return code 0 means ERROR_SUCCESS
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${If} $Result != 3010
  ${AndIf} $Result != 0
# NB: Return code 1603 (0x643) ignored as well
  ${Andif} $Result != 1603
    MessageBox MB_ICONEXCLAMATION "National Instruments Runtime Engine ERROR: $Message"
  ${Endif}
  ${If} $Architecture == "64"
    SetRegView 64
  ${Endif}
SectionEnd

Section -FTDISetup
#
# Install FTDI USB drivers
  DetailPrint "admin-FTDISetup"
# Disable COM port enumeration by means of 2 entries in the registry (Aug 2016)
  WriteRegBin HKLM ${FTDI_ENUM_KEY} ${FTDI_ENUM_REG1} ${FTDI_ENUM_VALUE}
  WriteRegBin HKLM ${FTDI_ENUM_KEY} ${FTDI_ENUM_REG2} ${FTDI_ENUM_VALUE}
# Install drivers
  ExecWait '"$FTDIDir\${FTDI_EXENAME}.exe /q" /q' $Result
  Sleep 3000
  StrCpy $Message "Install FTDI USB drivers: $Result"
# NB: Return code 512 means:
# - 0 driver packages successfully installed on a device
# - 2 driver packages copied to the driver store
# - 0 driver packages failed to install
  DetailPrint $Message
  ${If} $Result != 512
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${AndIf} $Result != 3010
    MessageBox MB_ICONEXCLAMATION "FTDI USB drivers ERROR: $Message"
  ${Endif}
SectionEnd

Section -PL2303Setup
#
# Install Serial-to-USB driver
  DetailPrint "admin-PL2303Setup"
# Install driver
  ExecWait '"$PL2303Dir\${PL2303_EXENAME}.exe /s" /q' $Result
  Sleep 3000
  StrCpy $Message "Install Prolific PL2303 Serial-to-USB driver: $Result"
  DetailPrint $Message
  ${If} $Result != 0
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${AndIf} $Result != 3010
    MessageBox MB_ICONEXCLAMATION "Prolific PL2303 Serial-to-USB driver ERROR: $Message"
  ${Endif}
SectionEnd

Section -CP210XSetup
#
# Install Silabs CP210x VCP USB driver
  DetailPrint "admin-CP210XSetup"
# Install driver
  ExecWait '"$CP210XDir\${CP210X_EXENAME}.exe" /q /se' $Result
  Sleep 3000
  StrCpy $Message "Install SiLabs CP210X VCP USB driver: $Result"
  DetailPrint $Message
# NB: Return code 256 means:
# - 0 driver packages successfully installed on a device
# - 1 driver packages copied to the driver store
# - 0 driver packages failed to install
  ${If} $Result != 256
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${AndIf} $Result != 3010
    MessageBox MB_ICONEXCLAMATION "SiLabsCP210X VCP USB driver ERROR: $Message"
  ${Endif}
SectionEnd

Section -TaskSetup
# Install task for Windows Task Scheduler (UAC: requires elevated permission/prompt)
# This is tricky: execute .bat --> calls PowerShell --> calls PowerShell to insert task in Windows Task Scheduler
# The Windows Task Scheduler executes .bat that executes Python code in which the status of services is checked
  ExecWait '"$TASKDir\${TASK1_CREATE}.bat"' $Result
  Sleep 3000
  StrCpy $Message "Install TASK1: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "TASK1 ERROR: $Message"
  ${Endif}
SectionEnd

Section -RegisterServices
#
# Post install: startup services
  DetailPrint "admin-RegisterServices"
# OpenVPN
  SimpleSC::SetServiceStartType "${VPN_SERVICENAME}" "2"
  Pop $0
  IntCmp $0 0 Done1 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not set service start OpenVPN - Reason: $0"
  Done1:
  Sleep 3000
  SimpleSC::StartService "${VPN_SERVICENAME}" "" "30"
  Pop $0
  IntCmp $0 0 Done2 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not start OpenVPN service - Reason: $0"
  Done2:
  Sleep 3000
# Check after 60 seconds if OpenVPN is running, if not then restart; not running after 5 mins then reboot
  SimpleSC::SetServiceFailure "${VPN_SERVICENAME}" "0" "" "" "1" "60000" "2" "300000" "0" "0"
  Pop $0
  IntCmp $0 0 Done3 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not set restart/reboot conditions OpenVPN service - Reason: $0"
  Done3:
  Sleep 3000
# TightVNC
  SimpleSC::SetServiceStartType "${VNC_SERVICENAME}" "2"
  Pop $0
  IntCmp $0 0 Done4 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not set service start TightVNC - Reason: $0"
  Done4:
  Sleep 3000
  SimpleSC::StartService "${VNC_SERVICENAME}" "" "30"
  Pop $0
  IntCmp $0 0 Done5 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not start TightVNC service - Reason: $0"
  Done5:
  Sleep 3000
# Check after 60 seconds if TightVNC is running, if not then restart; not running after 5 mins then reboot
  SimpleSC::SetServiceFailure "${VNC_SERVICENAME}" "0" "" "" "1" "60000" "2" "300000" "0" "0"
  Pop $0
  IntCmp $0 0 Done6 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not set restart/reboot conditions TightVNC service - Reason: $0"
  Done6:
  Sleep 3000
# Check after 60 seconds if Nagios Client++ is running, if not then restart; not running after 5 mins then reboot
  SimpleSC::SetServiceFailure "${NSCP_SERVICENAME}" "0" "" "" "1" "60000" "2" "300000" "0" "0"
  Pop $0
  IntCmp $0 0 Done7 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not set restart/reboot conditions Nagios Client service - Reason: $0"
  Done7:
  Sleep 3000
SectionEnd
