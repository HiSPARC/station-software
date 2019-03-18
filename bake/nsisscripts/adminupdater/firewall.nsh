#########################################################################################
#
# HiSPARC admin installer
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Included in admininstaller.nsh:
# - Set/Remove Windows firewall rules:
#   - Ping, profiles etc.
#   - Nagios Ports 5666 and 12489
#   - TightVNC port 5900
#   - ICMPv4/ICMPv6
#   - MySQL
#
#########################################################################################
#
# Sep 2016: - Facing problems with some Windows 10 installations; tried to circumvent
#             using either SimpleFC or PowerShell ---> both did not work...
#             Wait for further Windows 10 developments?
# Aug 2017: - After installing new version of OpenVPN Windows 10 seems to work
# Sep 2017: - Additional firewall settings
#           - Partly replace NSIS SimpleFC by netsh advfirewall commands
# Apr 2018: - When installing HiSPARC package, reset firewall to default
#           - Make more extensive use of 'netsh advfirewall' instructions
#           - Avoid re-installation firewall rule duplication: reset firewall to default
# Mar 2019: - Reset firewall to default when uninstalling HiSPARC software
#
#########################################################################################

Section -FirewallRules
#
# Configure Windows firewall for the HiSPARC programs
  DetailPrint "admin-FireWallRules"
# Check if the firewall is running...
  SimpleFC::IsFirewallServiceRunning
  Pop $1
  ${If} $1 == 0
# Windows firewall is not running; switch on!
    ExecWait 'netsh advfirewall firewall set all profiles state on'
  ${EndIf}
# Restore Windows firewall to default settings
  ExecWait 'netsh advfirewall reset'
# Enable inbound echo request
  ExecWait 'netsh advfirewall firewall add rule name="ICMP Allow incoming V4 echo request" protocol=icmpv4:8,any dir=in action=allow profile=public,private,domain'
  ExecWait 'netsh advfirewall firewall add rule name="ICMP Allow incoming V6 echo request" protocol=icmpv6:8,any dir=in action=allow profile=public,private,domain'
# Enable inbound router request
  ExecWait 'netsh advfirewall firewall add rule name="ICMP Allow incoming V4 router request" protocol=icmpv4:9,any dir=in action=allow profile=public,private,domain'
  ExecWait 'netsh advfirewall firewall add rule name="ICMP Allow incoming V6 router request" protocol=icmpv6:9,any dir=in action=allow profile=public,private,domain'
# Following Windows firewall rules are required for HiSPARC apllications
# Add Nagios Client++ ports and enable firewall rules
  ExecWait 'netsh advfirewall firewall add rule name="Nagios" dir=in action=allow protocol=TCP localport=5666 profile=public,private,domain remoteip=194.171.82.1 enable=yes'
  ExecWait 'netsh advfirewall firewall add rule name="Nagios" dir=in action=allow protocol=TCP localport=12489 profile=public,private,domain remoteip=194.171.82.1 enable=yes'
# Add TightVNC port and enable firewall rule
  ExecWait 'netsh advfirewall firewall add rule name="TightVNC" dir=in action=allow protocol=TCP localport=5900 profile=public,private,domain remoteip=172.16.66.0/24 enable=yes'
# MySQL Windows firewall rule is treated in the "userunpacker" firewall section
SectionEnd

Section un.FirewallRules
#
# Explicitly remove Nagios and VNC ports
  DetailPrint "admin-un.FirewallRules"
  SimpleFC::RemovePort  5666 6
  SimpleFC::RemovePort 12489 6
  SimpleFC::RemovePort  5900 6
# Check if the firewall is running...
  SimpleFC::IsFirewallServiceRunning
  Pop $1
  ${If} $1 == 0
# Windows firewall is not running; switch on!
    ExecWait 'netsh advfirewall firewall set all profiles state on'
  ${EndIf}
# Restore Windows firewall to default settings
  ExecWait 'netsh advfirewall reset'
SectionEnd
