#
#	interface2.nsh ------
#	MUI2: NSIS Modern User Interface 2.0
#

!include "MUI2.nsh"

; MUI Settings
!define MUI_ICON						hisparc.ico
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP			header.bmp
!define MUI_WELCOMEFINISHPAGE_BITMAP	welcome.bmp
!define MUI_UNWELCOMEFINISHPAGE_BITMAP	welcome.bmp
!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
#!insertmacro MUI_PAGE_DIRECTORY	Fixed installation path!
Page custom userinput1   "" ": Settings"
Page custom userinput2   "" ": Local Database Settings"
Page custom userinput3   "" ": Sensors"
Page custom startinstall "" ": Ready for installation"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------