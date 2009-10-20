!include "FileFunc.nsh"
!include "LogicLib.nsh"

Var /GLOBAL driveFound
Var /GLOBAL driveSearchingFor

Function TrimText
 Exch $R0 ; char
 Exch
 Exch $R1 ; length
 Exch 2
 Exch $R2 ; text
 Push $R3
 Push $R4

 StrLen $R3 $R2
 IntCmp $R3 $R1 Done Done

 StrCpy $R2 $R2 $R1

 StrCpy $R3 0
  IntOp $R3 $R3 + 1
  StrCpy $R4 $R2 1 -$R3
  StrCmp $R4 "" Done
  StrCmp $R4 $R0 0 -3

  IntOp $R3 $R3 + 1
  StrCpy $R4 $R2 1 -$R3
  StrCmp $R4 "" Done
  StrCmp $R4 $R0 -3

  IntOp $R3 $R3 - 1
  StrCpy $R2 $R2 -$R3
  StrCpy $R2 $R2...

 Done:
 StrCpy $R0 $R2
 Pop $R4
 Pop $R3
 Pop $R2
 Pop $R1
 Exch $R0 ; output
FunctionEnd

!macro TrimText Text Length Char Var
Push "${Text}"
Push "${Length}"
Push "${Char}"
 Call TrimText
Pop "${Var}"
!macroend
!define TrimText "!insertmacro TrimText"

Function FoundDrive
  ${If} $driveFound = 0
    ${If} "$driveSearchingFor" == "$9"
      StrCpy $driveFound 1
    ${Else}
      StrCpy $driveFound 0
    ${EndIf}
  ${EndIf}
  Push $0
FunctionEnd

!macro _DriveExists drivename
  StrCpy $driveSearchingFor "${driveName}"
  StrCpy $driveFound 0
  ${GetDrives} "ALL" "FoundDrive"
  Push $driveFound
!macroend

!macro _TryDrive drivename
  ${If} $selectedDrive == "none"
    ${DriveExists} "${drivename}"
    Pop $driveFound
    ${If} $driveFound == 0
      StrCpy $selectedDrive "${drivename}"
    ${EndIf}
  ${EndIf}
!macroend

!define TryDrive     `!insertmacro _TryDrive`
!define DriveExists     `!insertmacro _DriveExists`

Function TryDrives
  StrCpy $selectedDrive "none"

  ${TryDrive} "Z:\"
  ${TryDrive} "Y:\"
  ${TryDrive} "X:\"
  ${TryDrive} "W:\"
  ${TryDrive} "V:\"
  ${TryDrive} "U:\"
  ${TryDrive} "T:\"
  ${TryDrive} "S:\"
  ${TryDrive} "R:\"
  ${TryDrive} "Q:\"
  ${TryDrive} "P:\"
  ${TryDrive} "O:\"
  ${TryDrive} "N:\"
  ${TryDrive} "M:\"
  ${TryDrive} "L:\"
  ${TryDrive} "K:\"
  ${TryDrive} "J:\"
  ${TryDrive} "I:\"
  ${TryDrive} "H:\"
  ${TryDrive} "G:\"
  ${TryDrive} "F:\"
  ${TryDrive} "E:\"
  ${TryDrive} "D:\"
  ${TryDrive} "B:\"
  ${TryDrive} "A:\"
  #MessageBox MB_OK "$selectedDrive"
  
  ${TrimText} $selectedDrive 1 " " $selectedDrive
  #MessageBox MB_OK "$selectedDrive"
FunctionEnd

Section -FindingAFreeDrive
  Call TryDrives
SectionEnd