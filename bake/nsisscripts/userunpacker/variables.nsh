;Var VIRTUALDRIVE
;Var InstallPathApplication

;Section -GetVirtualDriveFromReg
;  !define FULLPRODUCTNAME "HiSPARC Client Application"
;  !define PRODUCTKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\${FULLPRODUCTNAME}\Path"
;  ReadRegStr $InstallPathApplication HKLM PRODUCTKEY ""
;  ReadINIStr $VIRTUALDRIVE "$InstallPathApplication\HiSPARC\Persistent\Configuration\config.ini" "Station" "VirtualDrive"
;SectionEnd

Var VIRTUALDRIVE
Var InstallPathApplication
;Var InstallationDirectory

Section -GetVirtualDriveFromReg
  !define FULLPRODUCTNAME "HiSPARC Client Application"
  !define PRODUCT_KEY "Software\${FULLPRODUCTNAME}"
  !define PRODUCT_ROOT_KEY "HKLM"
  ReadRegStr $InstallPathApplication ${PRODUCT_ROOT_KEY} "${PRODUCT_KEY}" "Path"
  ReadINIStr $VIRTUALDRIVE "$InstallPathApplication\hisparc\persistent\configuration\config.ini" "Station" "VirtualDrive"
  DetailPrint "The drive is: $VIRTUALDRIVE"

  !define InstallationDirectory "$VIRTUALDRIVE:\user"
  
  !define CONFIGINI "$VIRTUALDRIVE:\persistent\configuration\config.ini"
SectionEnd