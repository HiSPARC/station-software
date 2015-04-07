import sys

from startStop import StartStop
from hslog import log, setLogMode, MODE_BOTH


def stop_service(name, service_name):
    """Stop a service

    :param name: common name for printing
    :param service_name: name of the Service

    """
    try:
        log('Stopping %s Service' % name)
        service_handler = StartStop()
        service_handler.serviceName = service_name
        result = service_handler.stopService()
        if result == 0:
            log('Status: running')
        elif result == 1:
            log('Status: stopped')
        else:
            log('The service was not found!')
    except:
        log('An exception was generated while stopping %s:' % name +
            str(sys.exc_info()[1]))


def stop_admin_services():
    """Stop the admin services"""

    setLogMode(MODE_BOTH)
    log('Stopping Admin-Mode applications...')

    stop_service('TightVNC', 'tvnserver')
    stop_service('Nagios', 'NSClientpp')
    stop_service('OpenVPN', 'OpenVPNService')


if __name__ == "__main__":
    stop_admin_services()
