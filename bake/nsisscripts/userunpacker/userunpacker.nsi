; Script generated by the HM NIS Edit Script Wizard.
SetCompressor lzma

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "HiSPARC - User Software"
!define PRODUCT_VERSION "${USER_VERSION}"
!define PRODUCT_PUBLISHER "Nikhef"
!define PRODUCT_WEB_SITE "http://www.hisparc.nl"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\HiSPARC Client Application"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

!include interface.nsh

!include variables.nsh

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "..\..\releases\userUnpacker_v${PRODUCT_VERSION}.exe"
InstallDir "$VIRTUALDRIVE:\user\"
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  ;!insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

Section -Main Section
    #Copy files to the appropriate folders
    SetOutPath ${InstallationDirectory}
    SetOverwrite on
    File /r /x .svn ..\..\..\user\*
SectionEnd

Section -Post
  WriteIniStr ${CONFIGINI} Version CurrentUser ${PRODUCT_VERSION}

  WriteUninstaller "$VIRTUALDRIVE:\persistent\uninstallers\useruninst.exe"
  ;WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  ;WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  ;WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  ;WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  ;WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  #HideWindow
  #MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
;!insertmacro MUI_UNGETLANGUAGE
  #MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  #Abort
FunctionEnd

Section un.Uninstall
  # delete de hele map
  #DetailPrint "Removed: $InstallPathApplication\hisparc\user"
  RmDir /r /REBOOTOK "$InstallPathApplication\hisparc\user"

  Delete "$InstallPathApplication\hisparc\persistent\uninstallers\useruninst.exe"

  SetAutoClose true
SectionEnd