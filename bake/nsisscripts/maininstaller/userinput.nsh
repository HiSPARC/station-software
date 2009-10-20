Function userinput1
    loginsettings_start:
    ;Display the InstallOptions dialog
    InstallOptions::dialog "$PLUGINSDIR\userinput1.ini"
    Pop $0
    
    # Lees de instellingen.
    ${If} $0 == "success"

        ReadINIStr $StationNummer "$PLUGINSDIR\userinput1.ini" "Field 1" "State"

        ReadINIStr $StationPaswoord "$PLUGINSDIR\userinput1.ini" "Field 2" "State"
        ### TODO: Insert password into the database
        
        # certificaat
        ReadINIStr $CertZip "$PLUGINSDIR\userinput1.ini" "Field 3" "State"

        ${If} $CertZip == ""
            MessageBox MB_OK "U moet een certificaat opgeven!"
            GoTo loginsettings_start
        ${EndIf}
    ${EndIf}
FunctionEnd

Function userinput2
    InstallOptions::dialog "$PLUGINSDIR\userinput2.ini"
    Pop $0

    # Lees de instellingen.
    ${If} $0 == "success"
          # lokale db
          ReadINIStr $LDBHost "$PLUGINSDIR\userinput2.ini" "Field 1" "State"
    ${EndIf}
FunctionEnd

Function userinput3
    InstallOptions::dialog "$PLUGINSDIR\userinput3.ini"
    Pop $0

    # Lees de instellingen.
    ${If} $0 == "success"
        ReadINIStr $HasHiSPARC "$PLUGINSDIR\userinput3.ini" "Field 2" "State"
        ReadINIStr $HasWeerStation "$PLUGINSDIR\userinput3.ini" "Field 3" "State"
        ReadINIStr $HasAardmagnetisch "$PLUGINSDIR\userinput3.ini" "Field 4" "State"
        ReadINIStr $HasBliksem "$PLUGINSDIR\userinput3.ini" "Field 5" "State"
    ${EndIf}
FunctionEnd

Function startinstall
    ;Display the InstallOptions dialog
    InstallOptions::dialog "$PLUGINSDIR\startinstall.ini"
    Pop $0
FunctionEnd
