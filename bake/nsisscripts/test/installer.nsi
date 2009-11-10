!include MUI2.nsh

!define PRODUCT_NAME "HiSPARC Test Installer"

Name "${PRODUCT_NAME}"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
OutFile install.exe

!define MUI_ICON hisparc.ico
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP header.bmp
!define MUI_WELCOMEFINISHPAGE_BITMAP welcome.bmp
!define MUI_UNWELCOMEFINISHPAGE_BITMAP welcome.bmp
!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "Dutch"

Section Install
	SetOutPath $INSTDIR
	File "Readme.txt"
	WriteUninstaller $INSTDIR\uninstall.exe
SectionEnd

;!include firewall.nsh

Section Uninstall
	RMDir /r /REBOOTOK $INSTDIR
SectionEnd