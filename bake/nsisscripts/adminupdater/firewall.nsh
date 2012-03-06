#
#   firewall.nsh ------
#   Set the relevant ports open.
#

Section -FirewallRules
  DetailPrint "admin-FireWallRules"
  SimpleFC::AddPort  5666 "HiSPARC Nagios" 6 2 2 194.171.82.1 1
  SimpleFC::AddPort 12489 "HiSPARC Nagios" 6 2 2 194.171.82.1 1
  SimpleFC::AddPort  5900 "HiSPARC VNC"    6 2 2 172.16.66.0/24 1
  SimpleFC::AllowDisallowIcmpInboundEchoRequest 1
SectionEnd

Section un.FirewallRules
  DetailPrint "admin-un.FirewallRules"
  SimpleFC::RemovePort  5666 6
  SimpleFC::RemovePort 12489 6
  SimpleFC::RemovePort  5900 6
SectionEnd