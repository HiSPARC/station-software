!define PRODUCT_NAME "HiSPARC Test Installer"

Name "${PRODUCT_NAME}"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
OutFile install.exe

Page Directory
Page Instfiles

Section Install
	SetOutPath $INSTDIR
	File "Readme.txt"
	WriteUninstaller $INSTDIR\uninstall.exe
SectionEnd

!include firewall.nsh

Section Uninstall
	RMDir /r /REBOOTOK $INSTDIR
SectionEnd