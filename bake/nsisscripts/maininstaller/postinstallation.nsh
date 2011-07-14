Section -CreateUserAccounts
    SetDetailsPrint none

    # admin
    ExecWait "net user ${ADMHISPARC_USERNAME} ${ADMHISPARC_PASSWORD} /add"
    ExecWait "net localgroup Administrators ${ADMHISPARC_USERNAME} /add"

    # user
    ExecWait "net user ${HISPARC_USERNAME} ${HISPARC_PASSWORD} /add"

    SetDetailsPrint both
SectionEnd

Section -AutologonEnabling
	StrCpy $CpuName "this computer"
	ReadRegStr $0 HKLM ${CPUNAMEKEY} "ComputerName"
	StrCmp $0 "" done
	StrCpy $CpuName $0
	
done:
    WriteRegStr HKLM ${AUTOLOGONKEY} DefaultUserName   "${HISPARC_USERNAME}"
    WriteRegStr HKLM ${AUTOLOGONKEY} DefaultPassword   "${HISPARC_PASSWORD}"
    WriteRegStr HKLM ${AUTOLOGONKEY} AutoAdminLogon    "1"
    WriteRegStr HKLM ${AUTOLOGONKEY} ForceAdminLogon   "1"
    WriteRegStr HKLM ${AUTOLOGONKEY} DefaultDomainName "$CpuName"
SectionEnd

