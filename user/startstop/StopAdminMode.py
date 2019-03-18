"""Stop the HiSPARC admin services:

     These services are stopped:
     TightVNC, Nagios, OpenVPN

"""

import logging

import startstop_logger
from startStop import StartStop

logger = logging.getLogger('startstop.stopadmin')


def stop_service(name, service_name):
    """Stop a service

    :param name: common name for printing
    :param service_name: name of the Service

    """
    try:
        logger.info('Stopping %s Service', name)
        service_handler = StartStop()
        service_handler.serviceName = service_name
        result = service_handler.stopService()
        if result == 0:
            logger.info('Status: running')
        elif result == 1:
            logger.info('Status: stopped')
        else:
            logger.error('The service was not found!')
    except:
        logger.exception('An exception was generated while stopping %s', name)


def stop_admin_services():
    """Stop the admin services"""

    logger.info('Stopping Admin-Mode applications...')

    stop_service('TightVNC', 'tvnserver')
    stop_service('Nagios', 'nscp')
    stop_service('OpenVPN', 'OpenVPNService')


if __name__ == "__main__":
    startstop_logger.setup()
    stop_admin_services()
