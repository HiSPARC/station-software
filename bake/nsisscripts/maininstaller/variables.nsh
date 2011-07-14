#
#	variables.nsh
#

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
Var CpuName

#
# Windows accounts and passwords
#
!define ADMHISPARC_USERNAME "admhisparc"
!define ADMHISPARC_PASSWORD "PLACEHOLDER"
!define HISPARC_USERNAME    "hisparc"
!define HISPARC_PASSWORD    "PLACEHOLDER"

#
# Register key of autologon.
#
!define AUTOLOGONKEY	"'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon'"
!define	CPUNAMEKEY		"'System\CurrentControlSet\Control\ComputerName\ActiveComputerName'"
