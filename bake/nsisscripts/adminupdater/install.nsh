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
    # deze opties kunnen niet door een gebruiker worden overgeschreven.
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" AllowEditClients 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" AllowLoopback 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" AllowProperties 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" AllowShutdown 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" AuthRequired 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" AutoPortSelect 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" ConnectPriority 1 # niemand disconnecten
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" DisableTrayIcon 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" HTTPConnect 0 # geen java viewer
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" IdleTimeout 0 # geen timeout
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" InputsEnabled 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" LockSetting 1 # lock pc als iedereen is uitgelogd
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" LoopbackOnly 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" RemoveWallpaper 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" SocketConnect 1

    # polling
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" PollUnderCursor 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" PollForeground 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" PollFullscreen 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" OnlyPollConsole 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" OnlyPollOnEvent 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" PollingCycle 300

    # het wachtwoord
    WriteRegBin HKLM "SOFTWARE\ORL\WinVNC3\Default" Password ${VNC_WACHTWOORD}
    WriteRegBin HKLM "SOFTWARE\ORL\WinVNC3\Default" PasswordViewOnly ${VNC_WACHTWOORD}

    # tightvnc specifieke settings
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" BlackScreen 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" DontSetHooks 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" DontSetDriver 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" DriverDirectAccess 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" EnableFileTransfers 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" LocalInputsDisabled 1
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" LocalInputsPriority 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" LocalInputsPriorityTime 3
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" QueryAccept 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" QueryAllowNoPass 0
    WriteRegDWORD HKLM "SOFTWARE\ORL\WinVNC3" QuerySetting 2

    WriteRegDWORD HKCU "Software\ORL\VNCHooks\Application_Prefs\WinVNC.exe" use_Deferral 1
    WriteRegDWORD HKCU "Software\ORL\VNCHooks\Application_Prefs\WinVNC.exe" use_GetUpdateRect 1
    WriteRegDWORD HKCU "Software\ORL\VNCHooks\Application_Prefs\WinVNC.exe" use_KeyPress 1
    WriteRegDWORD HKCU "Software\ORL\VNCHooks\Application_Prefs\WinVNC.exe" use_LButtonUp 1
    WriteRegDWORD HKCU "Software\ORL\VNCHooks\Application_Prefs\WinVNC.exe" use_MButtonUp 1
    WriteRegDWORD HKCU "Software\ORL\VNCHooks\Application_Prefs\WinVNC.exe" use_RButtonUp 1
    WriteRegDWORD HKCU "Software\ORL\VNCHooks\Application_Prefs\WinVNC.exe" use_Timer 0

    # service
    ExecWait '"$InstallPathApplication\hisparc\admin\tightvnc\Winvnc.exe" -install'

    #DetailPrint "TightVNC service geinstalleerd."
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

    WriteRegStr HKLM ${ODBCREGKEY} DATABASE "buffer"
    WriteRegStr HKLM ${ODBCREGKEY} DESCRIPTION "HiSPARC buffer"
    WriteRegStr HKLM ${ODBCREGKEY} Driver '${ODBCDRVPATH}'
    WriteRegStr HKLM ${ODBCREGKEY} PORT 3306
    WriteRegStr HKLM ${ODBCREGKEY} PWD '${BUFFERPASS}'
    WriteRegStr HKLM ${ODBCREGKEY} SERVER "${BDBHOST}"
    WriteRegStr HKLM ${ODBCREGKEY} UID "buffer"

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
    SimpleSC::SetServiceStartType ${VNCSERVICENAME} 2
    SimpleSC::StartService ${VNCSERVICENAME}
    SimpleSC::GetErrorMessage

    # zet de nscp service op automatisch en start de service.
    SimpleSC::SetServiceStartType ${NSCPSERVICENAME} 2
    SimpleSC::StartService ${NSCPSERVICENAME}
    SimpleSC::GetErrorMessage
SectionEnd