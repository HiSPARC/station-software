from definitions import *
import settings
from diagnosticcheck import DiagnosticCheck

import pythoncom
import wmi
import _winreg
import logging
logger = logging.getLogger("proxy")

class Check(DiagnosticCheck):
    """Run proxy settings diagnostics

    This check tries to determine if a proxy server is needed for network
    access.  If the VPN connection is not working, this check might tell
    you how to configure VPN for internet access.

    """
    name = "Proxy settings"

    def _check(self):
        pythoncom.CoInitialize()
        r = wmi.WMI(namespace="DEFAULT").StdRegProv
        hDefKey = _winreg.HKEY_CURRENT_USER
        sSubKeyName = "SOFTWARE/Microsoft/Windows/CurrentVersion/Internet Settings"
        enabled = r.GetDWORDValue(hDefKey, sSubKeyName, 'ProxyEnable')[1]
        server = r.GetStringValue(hDefKey, sSubKeyName, 'ProxyServer')[1]

        self.server = server
        if enabled is None:
            enabled = 0
        self.enabled = [False, True][enabled]
        enabled = ["disabled", "enabled"][enabled]
        self.message = "Proxy (%s) is %s" % (server, enabled)

        pythoncom.CoUninitialize()
        return status.SUCCESS
