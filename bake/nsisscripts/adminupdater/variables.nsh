#
!define VNC_PASSWORD        "PLACEHOLDER"

!define TIGHTVNCKEY      	"'SOFTWARE\TightVNC'"
!define TVNCCOMPONENTSKEY	"'SOFTWARE\TightVNC\Components'"
!define TVNCSERVERKEY    	"'SOFTWARE\TightVNC\Server'"

Var TvncFolder
Var Program

#
# Register key van odbc.
#
!define ODBCDRV "MySQL ODBC 5.1 Driver"
!define ODBCREGKEY "SOFTWARE\ODBC\ODBC.INI\buffer"
!define ODBCDSREGKEY "SOFTWARE\ODBC\ODBC.INI\ODBC Data Sources"
!define ODBCDRVPATH "C:\WINDOWS\system32\myodbc5.dll"

!define BUFFERPASS "PLACEHOLDER"
!define BDBHOST "localhost"

Var VIRTUALDRIVE
Var InstallPathApplication
;Var InstallationDirectory
Var CertZip
Var NIDIR

Section -GetVirtualDriveFromReg
  !define FULLPRODUCTNAME "HiSPARC Client Application"
  !define PRODUCT_KEY "Software\${FULLPRODUCTNAME}"
  !define PRODUCT_ROOT_KEY "HKLM"
  ReadRegStr $InstallPathApplication ${PRODUCT_ROOT_KEY} "${PRODUCT_KEY}" "Path"
  ReadINIStr $VIRTUALDRIVE "$InstallPathApplication\hisparc\persistent\configuration\config.ini" "Station" "VirtualDrive"
  DetailPrint "The drive is: $VIRTUALDRIVE"
  
  !define InstallationDirectory "$VIRTUALDRIVE:\admin"
  
  !define CONFIGINI "$VIRTUALDRIVE:\persistent\configuration\config.ini"
SectionEnd

Section -GetCertificate
  ReadINIStr $CertZip "$InstallPathApplication\hisparc\persistent\configuration\config.ini" "Station" "Certificate"
SectionEnd
;!define CertZip "$VIRTUALDRIVE\persistent\configuration\certificate.zip"

# Namen van de services
!define VPNSERVICENAME		"OpenVPNService"
!define VNC_SERVICENAME     "tvnserver"
!define NSCPSERVICENAME 	"NSClientpp"
