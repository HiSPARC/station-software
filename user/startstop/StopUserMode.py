"""Stop the HiSPARC user executables.

These applications are stopped:
HiSPARC Detector, HiSPARC Weather, MySQL, HiSPARC Monitor, HiSPARC Updater

"""

import logging

import startstop_logger
from startStop import StartStop, CMDStartStop, status

logger = logging.getLogger('startstop.stopuser')


def stop_executable(name, exe_name, title=None):
    """Stop an executable

    :param name: common name for the program
    :param exe_name: name of the process
    :param title: specific name of the window to stop

    """
    try:
        logger.info('Stopping %s...', name)
        if title is None:
            handler = StartStop()
        else:
            handler = CMDStartStop()
            handler.title = title
        handler.exeName = exe_name
        result = handler.stopProcess()
        logger.info('Status: %s', status(result))
    except:
        logger.exception('An exception was generated while stopping %s!', name)


def stop_executables():
    """Stop the user executables"""

    logger.info('Stopping User-Mode applications...')

    stop_executable('HiSPARC Detector', 'hisparcdaq.exe')
    stop_executable('HiSPARC Weather', 'HiSPARC Weather Station.exe')
    stop_executable('MySQL', 'mysqld.exe')
    stop_executable('HiSPARC Monitor', 'python.exe', 'HiSPARC Monitor')
    stop_executable('HiSPARC Updater', 'python.exe', 'HiSPARC Updater')


if __name__ == "__main__":
    startstop_logger.setup()
    stop_executables()
