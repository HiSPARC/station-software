!define CONFIGINI "$selectedDrive:\persistent\configuration\config.ini"
#!define installerScriptPath "nsisinstaller"

Var LDBHOST
Var KeepBufferData
Var StationNummer
Var HasHiSPARC
Var HasWeerStation
Var HasAardmagnetisch
Var HasBliksem
Var StationPaswoord
Var CertZip
Var selectedDrive

#
# Windows accounts en wachtwoorden.
#
!define ADMHISPARC_USERNAME "admhisparc"
!define ADMHISPARC_PASSWORD "PLACEHOLDER"
!define HISPARC_USERNAME "hisparc"
!define HISPARC_PASSWORD "PLACEHOLDER"

#
# Register key van autologon.
#
!define AUTOLOGONKEY "'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon'"
