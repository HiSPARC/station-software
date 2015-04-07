import sys

from startStop import StartStop
from hslog import log, setLogMode, MODE_BOTH


def start_service(name, service_name):
    """Start a service

    :param name: common name for printing
    :param service_name: name of the Service

    """
    try:
        log('Starting %s Service' % name)
        service_handler = StartStop()
        service_handler.serviceName = service_name
        result = service_handler.startService()
        if result == 0:
            log('Status: running')
        elif result == 1:
            log('Status: stopped')
        else:
            log('The service was not found!')
    except:
        log('An exception was generated while starting %s:' % name +
            str(sys.exc_info()[1]))


def start_admin_services():
    """Start the admin services"""

    setLogMode(MODE_BOTH)
    log('Starting Admin-Mode applications...')

    start_service('TightVNC', 'tvnserver')
    start_service('Nagios', 'NSClientpp')
    start_service('OpenVPN', 'OpenVPNService')


if __name__ == "__main__":
    start_admin_services()
