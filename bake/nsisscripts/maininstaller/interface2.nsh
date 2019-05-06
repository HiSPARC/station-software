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
# Apr 2019: - Installation instructions (NL + UK)
#           - Instruction files internet connection (NL + UK)
#
#########################################################################################

!include "MUI2.nsh"
!include "MUI_EXTRAPAGES.nsh"

# MUI Settings
!define MUI_ICON                        hisparc.ico
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP          header.bmp
!define MUI_WELCOMEFINISHPAGE_BITMAP    welcome.bmp
!define MUI_UNWELCOMEFINISHPAGE_BITMAP  welcome.bmp
!define MUI_ABORTWARNING

# Welcome page
!insertmacro MUI_PAGE_WELCOME

# Installation instructions
!insertmacro MUI_PAGE_README "SoftwareInstaller-NL.txt"
!insertmacro MUI_PAGE_README "SoftwareInstaller-UK.txt"

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
${ReadmeLanguage} "${LANG_ENGLISH}" \
          "                      IMPORTANT!" \
          "$\n Please carefully read following installation instructions!"


# MUI end ------
