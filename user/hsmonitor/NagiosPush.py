import logging
import json

import requests
from requests.exceptions import ConnectionError, Timeout

logger = logging.getLogger('hsmonitor.nagiospush')


NRDP_TOKEN = 'nrdp4hisp'  # not secret because used inside VPN


class NagiosPush(object):
    """send service status (passive checkresult) to nagios using NRDP"""

    def __init__(self, config):
        self.url = self._getNRDPUrl(config)
        self.machine_name = config["machine_name"]

    def sendToNagios(self, nagiosResult):
        """HTTP POST service status to nagios server"""

        params = {
           'token': NRDP_TOKEN,
           'cmd': 'submitcheck',
           'JSONDATA': self._createNRDPJSON(nagiosResult),
        }

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            requests.post(self.url, params=params, headers=headers, timeout=1)
        except (ConnectionError, Timeout) as exc:
            logger.warning('Unable to upload status for service %s (%s)'
                           % (nagiosResult.serviceName, exc))
        else:
            logger.debug('Check %s: Status code: %i, Status description: %s.\n'
                         % (nagiosResult.serviceName,
                            nagiosResult.status_code,
                            nagiosResult.description))

    def _createNRDPJSON(self, nagiosResult):
        """create JSON payload for NRDP passive checkresult"""

        nrdp_json = {
            "checkresults": [
                {
                    "checkresult": {
                        "type": "service",
                        "checktype": "passive"
                    },
                    "hostname": -1,
                    "servicename": -1,
                    "state": -1,
                    "output": -1
                }
            ]
        }

        nrdp_json['checkresults'][0]['hostname'] = self.machine_name
        nrdp_json['checkresults'][0]['servicename'] = nagiosResult.serviceName
        nrdp_json['checkresults'][0]['state'] = nagiosResult.status_code
        nrdp_json['checkresults'][0]['output'] = nagiosResult.description

        return json.dumps(nrdp_json)

    def _getNRDPUrl(self, config):
        """get NRDP URL from config

        if url is missing from config: create it from NSCA hostname
        for backwards compatibility.
        If no config, try hardcoded tietar VPN IP.

        """
        url = config.get('url', None)

        if url is None:
            nsca_host = config.get('host', '194.171.82.1')
            url = 'http://{}/nrdp'.format(nsca_host)

        logger.debug('Nagios NRDP URL: %s.' % url)
        return url
