!include "MUI2.nsh"

; MUI Settings
!define MUI_ICON hisparc.ico
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP header.bmp
!define MUI_WELCOMEFINISHPAGE_BITMAP welcome.bmp
!define MUI_UNWELCOMEFINISHPAGE_BITMAP welcome.bmp
!define MUI_ABORTWARNING

; Language Selection Dialog Settings
;!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
;!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
;!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
Page custom userinput1 "" ": Instellingen"
Page custom userinput2 "" ": Lokale Database Instellingen"
Page custom userinput3 "" ": Sensoren"
Page custom startinstall "" ": Klaar voor installatie"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "Dutch"
;!insertmacro MUI_LANGUAGE "English"

; MUI end ------