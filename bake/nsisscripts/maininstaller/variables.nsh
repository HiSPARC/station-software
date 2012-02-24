#
#	variables.nsh ------
#
Var HisparcDir
Var	ConfigFile
Var StationNumber
Var StationPassword
Var HasHiSPARC
Var HasWeatherStation
Var HasEarthMagnetic
Var HasLightning
Var CertZip
Var LDBHOST
Var CpuName
Var Result
Var	FileName
Var	CurVersion

#
# Windows accounts and passwords.
#
!define ADMHISPARC_USERNAME "admhisparc"
!define ADMHISPARC_PASSWORD "PLACEHOLDER"
!define HISPARC_USERNAME    "hisparc"
!define HISPARC_PASSWORD    "PLACEHOLDER"

#
# Registry key of autologon and variables.
#
!define AUTOLOGON_KEY		"'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon'"
!define	ALV_USER_NAME		"DefaultUserName"
!define	ALV_PASSWORD		"DefaultPassword"
!define	ALV_AUTO_ADMIN		"AutoAdminLogon"
!define	ALV_FORCE_ADMIN		"ForceAdminLogon"
!define	ALV_DOMAIN_NAME		"DefaultDomainName"

#
# Registry key of computer name and variable.
#
!define	CPUNAME_KEY			"'System\CurrentControlSet\Control\ComputerName\ActiveComputerName'"
!define	CPV_CPUNAME			"ComputerName"
