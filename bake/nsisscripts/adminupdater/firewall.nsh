#
#   firewall.nsh ------
#   Open the relevant ports.
#   Sep 2016: - tested extended firewall definitions to circumvent (hidden) Windows 10 firewall rules
#             - did not get it to work with SimpleFC neither with PowerShell ---> future work/avoid Windows 10?
#

Section -FirewallRules
#
# Add Nagios and VNC ports/applications, and enable rules
  DetailPrint "admin-FireWallRules"
  Execwait 'netsh advfirewall firewall set rule group="Network Discovery" new enable=No'
  SimpleFC::AddPort  5666 "HiSPARC Nagios" 6 2 2 194.171.82.1 1
  SimpleFC::AddPort 12489 "HiSPARC Nagios" 6 2 2 194.171.82.1 1
  SimpleFC::AddPort  5900 "HiSPARC VNC"    6 2 2 172.16.66.0/24 1
  SimpleFC::AllowDisallowIcmpInboundEchoRequest 1
  SimpleFC::AllowDisallowIcmpInboundRouterRequest 1
#  ReadRegDWORD $Major HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentMajorVersionNumber
#  IfErrors lbl_done 0
#  StrCpy $WinVersion "$Major"
#
#  Modify Windows firewall rules for (potentially hidden) Windows 10.0 'security features'
#  ${If} $WinVersion == "10"
#    MessageBox MB_ICONEXCLAMATION "Windows version $WinVersion!"
#    SimpleFC::AddPort  5666 "HiSPARC Nagios" 6 3 2 194.171.82.1 1
#    SimpleFC::AddPort 12489 "HiSPARC Nagios" 6 3 2 194.171.82.1 1
#    SimpleFC::AdvAddRule "File and Printer Sharing (Echo Request - ICMPv4-In)" "" 1 1 1 2147483647 1 "" "*" 8 "" "" "" "LocalSubnet" ""
#    SimpleFC::AdvAddRule "File and Printer Sharing (Echo Request - ICMPv6-In)" "" 58 1 1 2147483647 1 "" "*" 128 "" "" "" "LocalSubnet" ""
#    SimpleFC::AdvAddRule "Networking - Echo Request (ICMPv4-In)" "" 1 1 1 2147483647 1 "" "*" 8 "" "" "" "" ""
#    SimpleFC::AdvAddRule "Networking - Echo Request (ICMPv6-In)" "" 58 1 1 2147483647 1 "" "*" 128 "" "" "" "" ""
#  ${Endif}
#  lbl_done:
SectionEnd

Section un.FirewallRules
  DetailPrint "admin-un.FirewallRules"
  SimpleFC::RemovePort  5666 6
  SimpleFC::RemovePort 12489 6
  SimpleFC::RemovePort  5900 6
SectionEnd