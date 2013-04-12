#
#   userinput.nsh ------
#   The Page functions.
#   Main parameters are mandatory (April 2013, RH).
#

Function userinput1
    !insertmacro MUI_HEADER_TEXT "Station data" "Enter station number, password and certificate."
    loginsettings_start:
    ;Display the InstallOptions dialog
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

Function userinput2
    !insertmacro MUI_HEADER_TEXT "Local database" "This field remains usually empty. Questions? Consult the HiSPARC team."
    InstallOptions::dialog "$PLUGINSDIR\userinput2.ini"
    Pop $0

    # Read the settings
    ${If} $0 == "success"
          # local database
          ReadINIStr $LDBHost "$PLUGINSDIR\userinput2.ini" "Field 1" "State"
    ${EndIf}
FunctionEnd

Function userinput3
    !insertmacro MUI_HEADER_TEXT "Connected detectors" "Tickmark the connected detectors. Usually it is only a HiSPARC detector."
    InstallOptions::dialog "$PLUGINSDIR\userinput3.ini"
    Pop $0

    # Read the settings
    ${If} $0 == "success"
        ReadINIStr $HasHiSPARC        "$PLUGINSDIR\userinput3.ini" "Field 2" "State"
        ReadINIStr $HasWeatherStation "$PLUGINSDIR\userinput3.ini" "Field 3" "State"
        ReadINIStr $HasEarthMagnetic  "$PLUGINSDIR\userinput3.ini" "Field 4" "State"
        ReadINIStr $HasLightning      "$PLUGINSDIR\userinput3.ini" "Field 5" "State"
    ${EndIf}
FunctionEnd

Function startinstall
    !insertmacro MUI_HEADER_TEXT "Ready for installation." ""
    ;Display the InstallOptions dialog
    InstallOptions::dialog "$PLUGINSDIR\startinstall.ini"
    Pop $0
FunctionEnd
