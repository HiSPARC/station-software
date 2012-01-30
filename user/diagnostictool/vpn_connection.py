import pythoncom
import wmi
import os
import re
import logging

from definitions import status
from diagnosticcheck import DiagnosticCheck

logger = logging.getLogger("vpn")

class Check(DiagnosticCheck):
    """Run vpn connection diagnostics

    This check confirms that the VPN connection is up and running.  It
    tries to determine if the openvpn client is up and running.  Failing
    that, it tries to contact the VPN server, and establish a connection.
    This helps in finding the point of failure: DNS resolution, routing,
    firewalls, etc.

    """
    name = "VPN connection"

    def _check(self):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        try:
            vpn_service = c.Win32_Service(Name="OpenVPNService")[0]
        except IndexError:
            self.message = "VPN service is not installed.  Please report."
            pythoncom.CoUninitialize()
            return status.FAIL
        if vpn_service.State != "Running":
            self.message = "VPN service is not running."
            pythoncom.CoUninitialize()
            return status.FAIL
        path = os.path.dirname(vpn_service.PathName).replace('\"', '')
        path = os.path.join(path, '../log/hisparc.log')
        vpnstatus = 'unknown'
        try:
            with open(path) as logfile:
                lines = logfile.readlines()
                for line in lines:
                    if re.search("Initialization Sequence Completed", line):
                        vpnstatus = 'ok'
                    if re.search("Connection reset", line):
                        vpnstatus = 'reset'
        except IOError, exc:
            self.message = "Could not open log file: %s" % exc
            pythoncom.CoUninitialize()
            return status.FAIL

        if vpnstatus == 'ok':
            self.message = "VPN connection established."
            pythoncom.CoUninitialize()
            return status.SUCCESS
        elif vpnstatus == 'reset' or vpnstatus == 'unknown':
            self.message = ("VPN connection NOT established.  "
                            "Error condition:\n%s" % ''.join(lines[-10:]))
            pythoncom.CoUninitialize()
            return status.FAIL

        pythoncom.CoUninitialize()
        return None
