#########################################################################################
#
# HiSPARC admin installer
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Included in admininstaller.nsh:
# MUI: NSIS Modern User Interface
#
#########################################################################################
#
# Jul 2017: - MUI2 2.0 ---> interface.nsh ---> interface2.nsh
#
#########################################################################################

!include "MUI2.nsh"

# MUI Settings
!define MUI_ICON   "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_ABORTWARNING

# Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT      HKLM
!define MUI_LANGDLL_REGISTRY_KEY       "${HISPARC_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

# Welcome page
!insertmacro MUI_PAGE_WELCOME
# Instfiles page
!insertmacro MUI_PAGE_INSTFILES
# Finish page
!insertmacro MUI_PAGE_FINISH
# Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES
# Language files
!insertmacro MUI_LANGUAGE "English"

# MUI end ------
