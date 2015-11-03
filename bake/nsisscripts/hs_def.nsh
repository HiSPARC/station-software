#
#   hs_def.nsh ------
#   General definition file for the HiSPARC installer.
#   R.Hart@nikhef.nl, NIKHEF, Amsterdam
#   Modified: October 2012
#

!define HISPARC_NAME                "HiSPARC"
!define HISPARC_PUBLISHER           "Nikhef"
!define HISPARC_WEB_SITE            "http://www.hisparc.nl"
!define HISPARC_ROOT                "HISPARC_ROOT"
!define HISPARC_KEY                 "SOFTWARE\${HISPARC_NAME}"
!define HISPARC_UNINST_KEY          "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${HISPARC_NAME}"
!define HISPARC_NSIS_RELEASE_DIR    "..\..\releases"

!define HS_ADMIN_UPDATER            "adminUpdater"
!define HS_USER_UNPACKER            "userUnpacker"

!define REG_PATH                    "Path"
!define REG_VOLATILE_PATH           "VolatilePath"
!define REG_DISPLAY_NAME            "DisplayName"
!define REG_HISPARC_VERSION         "HiSPARCVersion"
!define REG_ADMIN_VERSION           "AdminVersion"
!define REG_USER_VERSION            "UserVersion"
!define REG_RELEASE                 "Release"
!define REG_RELEASE_DATE            "ReleaseDate"
!define REG_STATION_NUMBER          "StationNumber"
!define REG_HAS_HISPARC             "HasHiSPARC"
!define REG_HAS_WEATHER             "HasWeather"
!define REG_HAS_LIGHTNING           "HasLightning"
