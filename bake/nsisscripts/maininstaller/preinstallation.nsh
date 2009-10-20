
!include "LogicLib.nsh"

#
# Map Virtual Drive
#
!include finddrive.nsh

Section -CreateVirtualDrive
  ExecWait "subst $selectedDrive: $\"$INSTDIR\hisparc$\""
SectionEnd

#
# Copy certificate to the right location
#
Section -CopyCert
  CopyFiles $CertZip "$selectedDrive:\persistent\configuration"
SectionEnd

#
# Write configuration file
#
Section -WriteConfigFile
  # Station instellingen
  WriteIniStr ${CONFIGINI} Station Nummer $StationNummer

  WriteIniStr ${CONFIGINI} Station VirtualDrive $selectedDrive
  
  WriteIniStr ${CONFIGINI} Station Password $StationPaswoord
  
  WriteIniStr ${CONFIGINI} Station Certificate $CertZip
  DetailPrint $CertZip

  # upload instellingen
  ${If} $LDBHOST == ""
     WriteIniStr ${CONFIGINI} Upload LocalDBUrl ""
  ${Else}
     WriteIniStr ${CONFIGINI} Upload LocalDBUrl $LDBHOST
  ${EndIf}

  # Aangesloten detectoren
  ${If} $HasHiSPARC == "1"
     WriteIniStr ${CONFIGINI} Detector Enabled 1
  ${Else}
     WriteIniStr ${CONFIGINI} Detector Enabled 0
  ${EndIf}

  ${If} $HasWeerStation == "1"
     WriteIniStr ${CONFIGINI} Weerstation Enabled 1
  ${Else}
     WriteIniStr ${CONFIGINI} Weerstation Enabled 0
  ${EndIf}

  ${If} $HasAardmagnetisch == "1"
     WriteIniStr ${CONFIGINI} Aardmagnetisch Enabled 1
  ${Else}
     WriteIniStr ${CONFIGINI} Aardmagnetisch Enabled 0
  ${EndIf}

  ${If} $HasBliksem == "1"
     WriteIniStr ${CONFIGINI} Bliksem Enabled 1
  ${Else}
     WriteIniStr ${CONFIGINI} Bliksem Enabled 0
  ${EndIf}
SectionEnd

# Writes the selected drive letter to a batch file
# Assumes $DriveLetter is set
Function WriteDriveLetterBatchFile
  StrCpy $0 "set HISPARC_DRIVE=$selectedDrive"
  ClearErrors
  FileOpen $1 "$selectedDrive:\persistent\configuration\startup_settings.bat" w #FIXME: change path to sensible place and filename
  IfErrors done
  FileWrite $1 $0
  FileClose $1
  done:
FunctionEnd

Section -WriteBatchFile
  Call WriteDriveLetterBatchFile
SectionEnd
