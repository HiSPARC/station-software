from definitions import *
import settings
from diagnosticcheck import DiagnosticCheck

from urllib2 import urlopen, URLError, HTTPError
import logging
logger = logging.getLogger("data_connection")

class Check(DiagnosticCheck):
    """Run data connection diagnostics

    This check confirms that the monitor software can indeed upload data
    to our central server at Nikhef.  By default, python's urllib2 tries
    to use proxies if the OS is configured to do so.

    """
    name = "Data connection"

    def _check(self):
        logger.debug("Trying to connect to %s" % settings.DATA_URL)
        try:
            answer = urlopen(settings.DATA_URL, timeout=10).read()
        except (URLError, HTTPError), exc:
            self.message = "Failed during connection attempt: %s" % exc
            return status.FAIL
        else:
            if answer == '400':
                self.message = "Connection OK"
                return status.SUCCESS
            else:
                self.message = "Unknown answer from server: %s" % answer
                return status.PARTIAL

        return None
