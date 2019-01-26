"""Start the HiSPARC admin services:

These services are started:
TightVNC, Nagios, OpenVPN

"""

import logging

import startstop_logger
from startStop import StartStop

logger = logging.getLogger('startstop.startadmin')


def start_service(name, service_name):
    """Start a service

    :param name: common name for printing
    :param service_name: name of the Service

    """
    try:
        logger.info('Starting %s Service' % name)
        service_handler = StartStop()
        service_handler.serviceName = service_name
        result = service_handler.startService()
        if result == 0:
            logger.info('Status: running')
        elif result == 1:
            logger.info('Status: stopped')
        else:
            logger.info('The service was not found!')
    except:
        logger.exception('An exception was generated while starting %s', name)


def start_admin_services():
    """Start the admin services"""

    logger.info('Starting Admin-Mode applications...')

    start_service('TightVNC', 'tvnserver')
    start_service('Nagios', 'nscp')
    start_service('OpenVPN', 'OpenVPNService')


if __name__ == "__main__":
    startstop_logger.setup()
    start_admin_services()
