#########################################################################################
#
# Global definitions for the 3 HiSPARC installers (admin, user and main)
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Oct 2012: - Modified
# Jun 2017: - Cosmetics
#
#########################################################################################

#
# HiSPARC package info
!define HISPARC_NAME                "HiSPARC"
!define HISPARC_PUBLISHER           "Nikhef"
!define HISPARC_WEB_SITE            "http://www.hisparc.nl"
!define HISPARC_ROOT                "HISPARC_ROOT"
!define HISPARC_KEY                 "SOFTWARE\${HISPARC_NAME}"
!define HISPARC_UNINST_KEY          "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${HISPARC_NAME}"
!define HISPARC_NSIS_RELEASE_DIR    "..\..\releases"

#
# Installers: admin and user
!define HS_ADMIN_UPDATER            "adminUpdater"
!define HS_USER_UNPACKER            "userUnpacker"

#
# Registry keys
!define REG_ADMIN_VERSION           "AdminVersion"
!define REG_USER_VERSION            "UserVersion"
!define REG_PATH                    "Path"
!define REG_VOLATILE_PATH           "VolatilePath"
!define REG_DISPLAY_NAME            "DisplayName"
!define REG_HISPARC_VERSION         "HiSPARCVersion"
!define REG_RELEASE                 "Release"
!define REG_RELEASE_DATE            "ReleaseDate"
!define REG_STATION_NUMBER          "StationNumber"
!define REG_HAS_DAQ                 "HasDAQ"
!define REG_HAS_WEATHER             "HasWeather"
!define REG_HAS_LIGHTNING           "HasLightning"
