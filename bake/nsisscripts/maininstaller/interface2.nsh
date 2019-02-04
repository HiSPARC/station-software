#########################################################################################
#
# HiSPARC main installer user interface
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Included in hisparcinstaller.nsh:
# MUI: NSIS Modern User Interface
#
#########################################################################################
#
# Jul 2017: - MUI2 2.0 ---> interface.nsh ---> interface2.nsh
# Apr 2018: - Remove local database from user interface
#
#########################################################################################

!include "MUI2.nsh"

# MUI Settings
!define MUI_ICON                        hisparc.ico
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP          header.bmp
!define MUI_WELCOMEFINISHPAGE_BITMAP    welcome.bmp
!define MUI_UNWELCOMEFINISHPAGE_BITMAP  welcome.bmp
!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
# Insertmacro MUI_PAGE_DIRECTORY    Fixed installation path!
Page custom userinput1   "" ": Settings"
Page custom userinput3   "" ": Sensors"
Page custom startinstall "" ": Ready for installation"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# Language files
!insertmacro MUI_LANGUAGE "English"

# MUI end ------
