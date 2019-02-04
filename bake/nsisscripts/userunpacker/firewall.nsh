#########################################################################################
#
# HiSPARC admin installer
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Included in userunpacker.nsh:
# - Set Windows firewall for mysqld to avoid user interaction at installation
#
#########################################################################################
#
# Jul 2017: MySQL Windows firewall rules added
# May 2018: Use netsh commands
#
#########################################################################################

Section -FirewallRules
#
# Add MySQL rule to Windows firewall...this will only work at the time
# of full installation as administrator rights are required!
  xtInfoPlugin::IsAdministrator
  Pop $0
  ${If} $0 == "true"
    DetailPrint "user-FireWallRules"
# Check if the firewall is running...
    SimpleFC::IsFirewallServiceRunning
    Pop $1
    ${If} $1 == 0
# Windows firewall is not running; switch on!
      ExecWait 'netsh advfirewall firewall set all profiles state on'
    ${EndIf}
# Add application
    ExecWait 'netsh advfirewall firewall add rule name="mysqld" program="$HisparcDir\user\mysql\bin\mysqld.exe" dir=in action=allow protocol=TCP profile=public,private,domain enable=yes'
    ExecWait 'netsh advfirewall firewall add rule name="mysqld" program="$HisparcDir\user\mysql\bin\mysqld.exe" dir=in action=allow protocol=UDP profile=public,private,domain enable=yes'
  ${EndIf}
SectionEnd
