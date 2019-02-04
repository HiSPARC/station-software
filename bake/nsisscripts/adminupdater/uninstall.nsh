#########################################################################################
#
# HiSPARC admin installer: uninstall.nsh
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Create the admin uninstaller
#
#########################################################################################
#
# Aug 2013: - Some applications still use the 32-bit registry
# Sep 2016: - OpenVPN now for 32 and 64 bits
# Jul 2017: - Introduce uniform naming convention service directories
#           - FTDI USB drivers                                            (x32 and x64)
# Oct 2017: - PL2303 driver for Davis Serial-to-USB cable                 (x32 and x64)
#           - CP210x driver for Davis Weather Station interface           (x32 and x64)
# Apr 2018: - Remove FTDI drivers                                         (x32 and x64)
#           - Remove Prolific PL2303 Serial-to-USB driver                 (x32 and x64)
#           - Remove SiLabs CP210X USB driver                             (x32 and x64)
#           - Remove NSClient++ (.msi)                                    (x32 and x64)
#           - IVI-Foundation removal tool version 5.8.0 for NI-Visa       (x32)
#           - Remaining Nat. Instr. and IVI-Visa folders will be removed  (x32 and x64)
#
#########################################################################################

Function un.onInit
#
# Initialise admin uninstaller section
  DetailPrint "admin-un.onInit"
  InitPluginsDir
# AdminUnInstaller requires administrator rights
  xtInfoPlugin::IsAdministrator
  Pop $0
  ${If} $0 == "false"
    MessageBox MB_ICONEXCLAMATION "You have no administrator rights!$\nAdmin-Uninstallation aborted."
    Quit
  ${EndIf}
# Check for 32/64-bit architecture
  System::Call "kernel32::GetCurrentProcess() i .s"
  System::Call "kernel32::IsWow64Process(i s, *i .r0)"
  StrCmp $0 "0" is32 is64
is32:
  SetRegView 32
  StrCpy $Architecture "32"
  Goto proCeed
is64:
  SetRegView 64
  StrCpy $Architecture "64"
proCeed:
# Get HiSPARC directory name and path
  ReadRegStr $HisparcDir HKLM "${HISPARC_KEY}" ${REG_PATH}
  StrCmp $HisparcDir "" noReg
  ${DirState} $HisparcDir $Result
# Check if HisparcDir exists
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $HisparcDir does not exist!$\nAdmin-Installer aborted."
    Quit
  ${Endif}
  DetailPrint "HisparcDir: $HisparcDir"
  StrCpy $AdminDir   "$HisparcDir\admin"
# Check if HiSPARC administrator directory exists
  ${DirState} $AdminDir $Result
  ${If} $Result < 0
    MessageBox MB_ICONEXCLAMATION "FATAL: Folder $AdminDir does not exist!$\nAdmin-Uninstaller aborted."
    Quit
  ${Endif}
  DetailPrint "AdminDir: $AdminDir"
# Get the service, drivers and utility directories:
  ${If} $Architecture == "32"
    StrCpy $OpenVPNDir "$AdminDir\openvpn\x32"
    StrCpy $TightVNCDir "$AdminDir\tightvnc\x32"
    StrCpy $NSCPDir "$AdminDir\nsclientpp\x32"
    StrCpy $ODBCDir "$AdminDir\odbcconnector\x32"
    StrCpy $NIRTEDir "$AdminDir\nirte\x32"
    StrCpy $FTDIDir "$AdminDir\ftdi_drivers\x32"
    StrCpy $DelProfDir "$AdminDir\delprof2\x32"
    StrCpy $PL2303Dir "$AdminDir\pl2303\x32"
    StrCpy $CP210XDir "$AdminDir\cp210x\x32"
    StrCpy $UtilDir "$AdminDir\utilities"
  ${Else}
    StrCpy $OpenVPNDir "$AdminDir\openvpn\x64"
    StrCpy $TightVNCDir "$AdminDir\tightvnc\x64"
    StrCpy $NSCPDir "$AdminDir\nsclientpp\x64"
    StrCpy $ODBCDir "$AdminDir\odbcconnector\x32"
    StrCpy $NIRTEDir "$AdminDir\nirte\x32"
    StrCpy $FTDIDir "$AdminDir\ftdi_drivers\x64"
    StrCpy $DelProfDir "$AdminDir\delprof2\x32"
    StrCpy $PL2303Dir "$AdminDir\pl2303\x32"
    StrCpy $CP210XDir "$AdminDir\cp210x\x64"
    StrCpy $UtilDir "$AdminDir\utilities"
  ${Endif}
  DetailPrint "OpenVPNDir: $OpenVPNDir"
  DetailPrint "TightVNCDir: $TightVNCDir"
  DetailPrint "NSCPDir: $NSCPDir"
  DetailPrint "ODBCDir: $ODBCDir"
  DetailPrint "NIRTEDir: $NIRTEDir"
  DetailPrint "FTDIDir: $FTDIDir"
  DetailPrint "DelProfDir: $DelProfDir"
  DetailPrint "PL2303Dir: $PL2303Dir"
  DetailPrint "CP210XDir: $CP210XDir"
  DetailPrint "UtilDir: $UtilDir"
  Return
noReg:
  MessageBox MB_ICONEXCLAMATION "FATAL: Registry entry ${REG_PATH} not set or defined!$\nAdmin-Uninstaller aborted."
  Quit
FunctionEnd

Section un.UninstServices
#
# Stop and remove services from the service list
  DetailPrint "admin-un.UninstServices"
# OpenVPN
  SimpleSC::RemoveService "${VPN_SERVICENAME}"
  Pop $0
  IntCmp $0 0 Done1 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not remove OpenVPN service - Reason: $0"
  Done1:
# TightVNC
  SimpleSC::RemoveService "${VNC_SERVICENAME}"
  Pop $0
  IntCmp $0 0 Done2 +1 +1
    Push $0
    SimpleSC::GetErrorMessage
    Pop $0
    MessageBox MB_ICONEXCLAMATION "Could not remove TightVNC service - Reason: $0"
  Done2:
SectionEnd

Section un.UninstOpenVPN
#
# Uninstall OpenVPN and TAP-Windows virtual ethernet driver
  DetailPrint "admin-un.UninstOpenVPN"
#
# Remove OpenVPN service
  ExecWait '"$OpenVPNDir\bin\openvpnserv2.exe" -remove' $Result
  Sleep 3000
  StrCpy $Message "Uninstall OpenVPNserv2: $Result"
  DetailPrint $Message
# NB: Return code 0 means success
# NB: Return code 1 means uninstaller through forked child process still active; requires more time...
  ${If} $Result != 0
  ${AndIf} $Result != 1
    MessageBox MB_ICONEXCLAMATION "OpenVPN ERROR: $Message"
  ${Endif}
# Delete registry keys
  DeleteRegKey HKLM ${OPENVPN_KEY}
  DeleteRegKey HKLM ${OPENVPNMS_KEY}
# Remove TAP-Windows virtual ethernet driver...
  ExecWait '"$OpenVPNDir\bin\${TAP_EXENAME}.exe" remove ${TAP}' $Result
  Sleep 3000
  StrCpy $Message "Remove TAP-Windows Virtual Ethernet Driver: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "TAP-Windows ERROR: $Message"
  ${Endif}
# Remove OpenVPN directories
  RMDir /r /REBOOTOK "$AdminDir\openvpn"
SectionEnd

Section un.UninstTightVNC
#
# Remove TightVNC service
  DetailPrint "admin-un.UninstTightVNC"
  ExecWait '"$TightVNCDir\${VNC_EXENAME}.exe" -remove -silent' $Result
  Sleep 3000
  StrCpy $Message "Uninstall TightVNC server: $Result"
  DetailPrint $Message
# NB: Return code 0 means success
# NB: Return code 1 means uninstaller through forked child process still active; requires more time...
  ${If} $Result != 0
  ${AndIf} $Result != 1
    MessageBox MB_ICONEXCLAMATION "TightVNC ERROR: $Message"
  ${Endif}
# Delete registry keys
  DeleteRegKey HKLM ${TIGHTVNC_KEY}
# Remove TightVNC directories
  RMDir /r /REBOOTOK "$AdminDir\tightvnc"
SectionEnd

Section un.UninstNSCP
#
# Remove Nagios Client++
  DetailPrint "admin-un.UninstNSCP"
# Remove Nagios Client++ service
  ExecWait 'msiexec.exe /x "$NSCPDir\${NSCP_EXENAME}.msi" /q' $Result
  Sleep 3000
  StrCpy $Message "Uninstall Nagios Client++: $Result"
  DetailPrint $Message
  ${If} $Result != 0
  ${AndIf} $Result != 1
    MessageBox MB_ICONEXCLAMATION "Nagios Client++ ERROR: $Message"
  ${Endif}
# Remove Nagios Client++ directory
  RMDir /r /REBOOTOK "$NSCPDir"
SectionEnd

Section un.UninstODBC
#
# Remove ODBC database connector?
# ODBC x32 only!
  SetRegView 32
# Delete registry keys
  DeleteRegKey   HKLM ${ODBC_KEY}
  DeleteRegValue HKLM "${ODBCDS_KEY}" "buffer"
# Remove ODBC service
  ExecWait '"$ODBCDir\${UNINSTALL_BAT}.bat"' $Result
  Sleep 3000
  StrCpy $Message "Uninstall ODBC: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "ODBC ERROR: $Message"
  ${Endif}
  DetailPrint "admin-un.UninstODBC"
# x32 or x64?
  ${If} $Architecture == "64"
    SetRegView 64
  ${Endif}
# Uninstall Visual C++ Redistributable Packages for Visual Studio 2013 (x32)
  ExecWait '"$ODBCDir\${VCRE_EXENAME}.exe" /uninstall /q' $Result
  Sleep 3000
  StrCpy $Message "Uninstall Visual Studio 2013 x32: $Result"
  DetailPrint $Message
  ${If} $Result != 0
    MessageBox MB_ICONEXCLAMATION "Visual Studio 2013 x32 ERROR: $Message"
  ${Endif}
  ${If} $Architecture == "64"
# Uninstall Visual C++ Redistributable Packages for Visual Studio 2013 (x64)
    ExecWait '"$ODBCDir\${VCRE64_EXENAME}.exe" /uninstall /q' $Result
    Sleep 3000
    StrCpy $Message "Uninstall Visual Studio 2013 x64: $Result"
    DetailPrint $Message
    ${If} $Result != 0
      MessageBox MB_ICONEXCLAMATION "Visual Studio 2013 x64 ERROR: $Message"
    ${Endif}
  ${Endif}
# Remove ODBC directory
  RMDir /r /REBOOTOK "$ODBCDir"
SectionEnd

Section un.UninstNIRTE
#
# Remove National Instruments (LabVIEW) Run-Time-Engine?
  DetailPrint "admin-un.UninstNIRTE"
# x32 only!
  SetRegView 32
# Read registry key
  ReadRegStr $NIDir HKLM "${LABVIEW_KEY}" ${LABVIEW_DIR}
# Remove National Instruments RTE service!
  ExecWait '"$NIDir\Shared\NIUninstaller\uninst.exe" /qb /x all' $Result
  Sleep 3000
  StrCpy $Message "Uninstall National Instruments RTE: $Result"
  DetailPrint $Message
# NB: Return code 0 means ERROR_SUCCESS
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${If} $Result != 3010
  ${AndIf} $Result != 0
    MessageBox MB_ICONEXCLAMATION "National Instruments RTE: $Message"
  ${Endif}
# Remove Visa-IVI foundation RTE service: it turns out there is NO silent option (yet)
#  ExecWait '"$NIRTEDir\${VISA_EXENAME}.exe" /x /q' $Result
#  Sleep 3000
#  StrCpy $Message "Uninstall Visa-IVI RTE: $Result"
#  DetailPrint $Message
# NB: Return code 0 means ERROR_SUCCESS
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
#  ${If} $Result != 3010
#  ${AndIf} $Result != 0
#    MessageBox MB_ICONEXCLAMATION "Visa-IVI RTE: $Message"
#  ${Endif}
# Remove National Instruments Run Time Engine directory
  RMDir /r /REBOOTOK "$NIDir"
# Remove National Instruments and IVI Foundation directories
  ${If} ${FileExists} '$PROGRAMFILES32\National Instruments'
    RMDir /r /REBOOTOK "$PROGRAMFILES32\National Instruments"
  ${EndIf}
  ${If} ${FileExists} '$PROGRAMFILES64\National Instruments'
    RMDir /r /REBOOTOK "$PROGRAMFILES64\National Instruments"
  ${EndIf}
  ${If} ${FileExists} '$PROGRAMFILES32\IVI Foundation'
    RMDir /r /REBOOTOK "$PROGRAMFILES32\IVI Foundation"
  ${EndIf}
  ${If} ${FileExists} '$PROGRAMFILES64\IVI Foundation'
    RMDir /r /REBOOTOK "$PROGRAMFILES64\IVI Foundation"
  ${EndIf}
# x32 or x64?
  ${If} $Architecture == "64"
# Delete registry keys
    DeleteRegKey HKLM "SOFTWARE\WOW6432Node\National Instruments"
    DeleteRegKey HKLM "SOFTWARE\WOW6432Node\VXIPNP_Alliance"
    SetRegView 64
  ${Endif}
# Delete registry key
  DeleteRegKey HKLM "SOFTWARE\National Instruments"

  SectionEnd

Section un.UninstFTDI
#
# Remove FTDI USB drivers
  DetailPrint "admin-un.UninstFTDI"
# Remove FTDI USB bus driver
  ExecWait '"$FTDIDir\${FTDI_EXENAME}.exe /u ftdibus.inf /d /q" /q' $Result
  Sleep 3000
  StrCpy $Message "Uninstall FTDI USB bus driver: $Result"
  DetailPrint $Message
# NB: Return code 0 means ERROR_SUCCESS
# NB: code 1641 means
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${If} $Result != 3010
  ${AndIf} $Result != 1641
  ${AndIf} $Result != 0
    MessageBox MB_ICONEXCLAMATION "FTDI USB bus driver ERROR: $Message"
  ${Endif}
# Remove FTDI USB port driver
  ExecWait '"$FTDIDir\${FTDI_EXENAME}.exe /u ftdiport.inf /d /q" /q' $Result
  Sleep 3000
  StrCpy $Message "Uninstall FTDI USB port drivers $Result"
  DetailPrint $Message
# NB: Return code 0 means ERROR_SUCCESS
# NB: code 1641 means
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${If} $Result != 3010
  ${AndIf} $Result != 1641
  ${AndIf} $Result != 0
    MessageBox MB_ICONEXCLAMATION "FTDI USB port driver ERROR: $Message"
  ${Endif}
SectionEnd

Section un.UninstPL2303
#
# Uninstall Serial-to-USB driver
  DetailPrint "admin-un.UninstPL2303"
# Install driver
  ExecWait '"$PL2303Dir\${PL2303_EXENAME}.exe -uninstall -removeonly" /q' $Result
  Sleep 3000
  StrCpy $Message "Uninstall Prolific PL2303 Serial-to-USB driver: $Result"
  DetailPrint $Message
# NB: Return code 0 means ERROR_SUCCESS
# NB: code 1641 means
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${If} $Result != 3010
  ${AndIf} $Result != 1641
  ${AndIf} $Result != 0
    MessageBox MB_ICONEXCLAMATION "Prolific PL2303 Serial-to-USB driver ERROR: $Message"
  ${Endif}
SectionEnd

Section un.UninstCP210X
#
# Uninstall Silabs CP210x VCP USB driver
  DetailPrint "admin-CP210XSetup"
# Install driver
  ExecWait '"$CP210XDir\${CP210X_EXENAME}.exe /u silabser.inf /d /q /se" /q' $Result
  Sleep 3000
  StrCpy $Message "Uninstall SiLabs CP210X VCP USB driver: $Result"
  DetailPrint $Message
# NB: Return code 0 means ERROR_SUCCESS
# NB: code 1641 means
# NB: Return code 3010 (0xBC2) means ERROR_SUCCESS_REBOOT_REQUIRED
  ${If} $Result != 3010
  ${AndIf} $Result != 1641
  ${AndIf} $Result != 0
    MessageBox MB_ICONEXCLAMATION "SiLabsCP210X VCP USB driver ERROR: $Message"
  ${Endif}
SectionEnd

Section un.UninstProgs
#
# Remove the entire admin folder
  DetailPrint "admin-un.UninstProgs"
# Remove admin directory
  RMDir /r /REBOOTOK "$AdminDir"
SectionEnd

Section un.Uninstall
#
# Remove admin uninstaller
  DetailPrint "admin-un.Uninstall"
  Delete "$HisparcDir\persistent\uninstallers\adminuninst.exe"
  SetAutoClose true
SectionEnd
