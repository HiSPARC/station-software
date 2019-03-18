#########################################################################################
#
# HiSPARC main installer user interface
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this interface does:
#  - Check for stationnumber, database password and certificate
#  - Define station configuration
#  - Check if config.ini exists
#
#########################################################################################
#
# Apr 2013: - Main parameters are mandatory
# Jul 2017: - MUI2 2.0 ---> interface.nsh ---> interface2.nsh
# Apr 2018: - Remove local database from user interface
# Feb 2019: - Replaced $HasLightning by $HasLightningDetector
#
#########################################################################################

Function userinput1
  !insertmacro MUI_HEADER_TEXT "Station data" "Enter station number, password and certificate."
  loginsettings_start:
# Display the InstallOptions dialog
  InstallOptions::dialog "$PLUGINSDIR\userinput1.ini"
  Pop $0
# Read the settings
  ${If} $0 == "success"
    ReadINIStr $StationNumber   "$PLUGINSDIR\userinput1.ini" "Field 1" "State"
    ReadINIStr $StationPassword "$PLUGINSDIR\userinput1.ini" "Field 2" "State"
    ReadINIStr $CertZip         "$PLUGINSDIR\userinput1.ini" "Field 3" "State"
    ${If} $StationNumber == ""
      MessageBox MB_OK "You must enter a station number!"
      GoTo loginsettings_start
    ${EndIf}
    ${If} $StationPassword == ""
      MessageBox MB_OK "You must enter a password!"
      GoTo loginsettings_start
    ${EndIf}
    ${If} $CertZip == ""
      MessageBox MB_OK "You must enter a certificate!"
      GoTo loginsettings_start
    ${EndIf}
    FileOpen $Result $CertZip r
    ${If} $Result == ""
      MessageBox MB_OK "Cannot open certificate, choose another!"
      GoTo loginsettings_start
    ${EndIf}
    FileClose $Result
  ${EndIf}
FunctionEnd

Function userinput3
  !insertmacro MUI_HEADER_TEXT "Connected detectors" "Tickmark the connected detectors. Usually it is only a HiSPARC detector."
  InstallOptions::dialog "$PLUGINSDIR\userinput3.ini"
  Pop $0
# Read the settings
  ${If} $0 == "success"
    ReadINIStr $HasHiSPARC           "$PLUGINSDIR\userinput3.ini" "Field 2" "State"
    ReadINIStr $HasWeatherStation    "$PLUGINSDIR\userinput3.ini" "Field 3" "State"
    ReadINIStr $HasLightningDetector "$PLUGINSDIR\userinput3.ini" "Field 4" "State"
  ${EndIf}
FunctionEnd

Function startinstall
  !insertmacro MUI_HEADER_TEXT "Ready for installation." ""
# Display the InstallOptions dialog
  InstallOptions::dialog "$PLUGINSDIR\startinstall.ini"
  Pop $0
FunctionEnd
