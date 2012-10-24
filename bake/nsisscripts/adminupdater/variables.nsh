#
#   variables.nsh ------
#   Admin installer
#
Var HisparcDir
Var AdminDir
Var NIdir
Var ConfigFile
Var CertZip
Var TvncFolder
Var Program
Var Result
Var FileName

# Names of the services
!define VPN_SERVICENAME     "OpenVPNService"
!define VNC_SERVICENAME     "tvnserver"
!define NSCP_SERVICENAME    "NSClientpp"

# OpenVPN definitions
!define OPENVPN_KEY         "SOFTWARE\OpenVPN"

# TightVNC definitions
!define VNC_CTRL_PASSWORD   "PLACEHOLDER"
!define VNC_PASSWORD        "PLACEHOLDER"
!define TIGHTVNC_KEY        "SOFTWARE\TightVNC"
!define TVNCCOMPONENTS_KEY  "SOFTWARE\TightVNC\Components"
!define TVNCSERVER_KEY      "SOFTWARE\TightVNC\Server"

# Register key of ODBC
!define ODBCDRV             "MySQL ODBC 5.1 Driver"
!define ODBCREGKEY          "SOFTWARE\ODBC\ODBC.INI\buffer"
!define ODBCDSREGKEY        "SOFTWARE\ODBC\ODBC.INI\ODBC Data Sources"
!define ODBCDRVPATH         "C:\WINDOWS\system32\myodbc5.dll"
!define BUFFERPASS          "PLACEHOLDER"
!define BDBHOST             "localhost"

# LabVIEW definitions
!define LABVIEW_KEY         "SOFTWARE\National Instruments\Common\Installer"
!define LABVIEW_DIR         "NIDIR"
