#
#   variables.nsh ------
#   Admin installer
#
Var WinVersion
Var HisparcDir
Var Architecture
Var AdminDir
Var NIdir
Var ConfigFile
Var CertZip
Var TvncFolder
Var TapWinDir
Var OpenVpnDir
Var Program
Var Result
Var FileName
Var FolderName
Var Message
Var Major

# Names of the services
!define VPN_SERVICENAME     "OpenVPNService"
!define VNC_SERVICENAME     "tvnserver"
!define NSCP_SERVICENAME    "NSClientpp"

# OpenVPN definitions
!define OPENVPN_KEY         "SOFTWARE\OpenVPN"
# Registry key to overcome hidden security measure blocking OpenVPN in Windows 10
!define GUEST_KEY_PATH      "SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters"
!define GUEST_KEY           "AllowInsecureGuestAuth"

# Attempt to kill microsoft spying in Windows 10
!define SPY_KEY_Path        "SOFTWARE\Policies\Microsoft\Windows\DataCollection"
!define SPY_KEY             "AllowTelemetry"

# TightVNC definitions
!define TIGHTVNC_KEY        "SOFTWARE\TightVNC"
!define TVNCCOMPONENTS_KEY  "SOFTWARE\TightVNC\Components"
!define TVNCSERVER_KEY      "SOFTWARE\TightVNC\Server"

# Register key of ODBC
!define ODBCDRV             "MySQL ODBC 5.1 Driver"
!define ODBCREGKEY          "SOFTWARE\ODBC\ODBC.INI\buffer"
!define ODBCDSREGKEY        "SOFTWARE\ODBC\ODBC.INI\ODBC Data Sources"
!define ODBCDRVPATH         "C:\WINDOWS\system32\myodbc5.dll"
!define BDBHOST             "localhost"

# LabVIEW definitions
!define LABVIEW_KEY         "SOFTWARE\National Instruments\Common\Installer"
!define LABVIEW_DIR         "NIDIR"

# FTDI definitions
!define FTDI_ENUM_VALUE     "01"
!define FTDI_ENUM_KEY       "SYSTEM\CurrentControlSet\Control\UsbFlags"
!define FTDI_ENUM_REG1      "IgnoreHWSerNum04036001"
!define FTDI_ENUM_REG2      "IgnoreHWSerNum04036010"

# NoLockScreen definitions
!define LOCKSCREEN_KEY      "SOFTWARE\Policies\Microsoft\Windows\Personalization"
!define LOCKSCREEN_REG      "NoLockScreen"
