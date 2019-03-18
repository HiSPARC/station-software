import logging
import json

import requests
from requests.exceptions import ConnectionError, Timeout

logger = logging.getLogger('hsmonitor.nagiospush')


class NagiosPush(object):
    """send service status (passive checkresult) to nagios using NRDP"""

    def __init__(self, config):
        self.url, self.backup_url = self._getNRDPUrl(config)
        self.machine_name = config["machine_name"]
        self.nrdp_token = config["nrdp_token"]

    def sendToNagios(self, nagiosResult):
        """HTTP POST service status to nagios server"""

        nrdp_json = {
            "checkresults": [
                {
                    "checkresult": {
                        "type": "service",
                        "checktype": "passive"
                    },
                    "hostname": self.machine_name,
                    "servicename": nagiosResult.serviceName,
                    "state": nagiosResult.status_code,
                    "output": nagiosResult.description
                }
            ]
        }

        params = {
           'token': self.nrdp_token,
           'cmd': 'submitcheck',
           'JSONDATA': json.dumps(nrdp_json),
        }

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            requests.post(self.url, params=params, headers=headers, timeout=5)
        except (ConnectionError, Timeout) as exc:
            logger.warning('Unable to upload status for service %s'
                           % nagiosResult.serviceName)
            logger.debug('Unable to upload status for service %s (%s)'
                           % (nagiosResult.serviceName, exc))
            # try other url on next attempt
            self.url, self.backup_url = self.backup_url, self.url
            logger.debug('Switching NRDP URLs. Next attempt will use %s'
                         % self.url)
        else:
            logger.debug('Check %s: Status code: %i, Status description: %s.\n'
                         % (nagiosResult.serviceName,
                            nagiosResult.status_code,
                            nagiosResult.description))

    def _getNRDPUrl(self, config):
        """get NRDP URLs from config

        if url is missing from config assume default.

        """
        url = config.get('URL', 'http://194.171.82.1/nrdp')
        backup_url = config.get('Backup_URL', 'http://vpn.hisparc.nl/nrdp')

        logger.debug('Nagios NRDP URL: %s / %s.' % (url, backup_url))
        return url, backup_url
