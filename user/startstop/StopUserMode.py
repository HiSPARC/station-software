"""Stop the HiSPARC user executables.

These applications are stopped:
HiSPARC DAQ, HiSPARC Weather, HiSPARC Lightning, MySQL, HiSPARC Monitor, HiSPARC Updater

"""

import logging

import startstop_logger
from startStop import StartStop, CMDStartStop, status

logger = logging.getLogger('startstop.stopuser')


def stop_executable(name, process_name, cmd=False):
    """Stop an executable

    :param name: common name for the program
    :param process_name: name of the process
    :param cmd: boolean indicating if it is a cmd window (e.g. Python)

    """
    try:
        logger.info('Stopping %s...', name)
        if not cmd:
            handler = StartStop()
            handler.exeName = process_name
        else:
            handler = CMDStartStop()
            handler.windowName = process_name
        result = handler.stopProcess()
        logger.info('Status: %s', status(result))
    except:
        logger.exception('An exception was generated while stopping %s!', name)


def stop_executables():
    """Stop the user executables"""

    logger.info('Stopping User-Mode applications...')

    stop_executable('HiSPARC Detector', 'HiSPARC DAQ.exe')
    stop_executable('HiSPARC Weather', 'HiSPARC Weather Station.exe')
    stop_executable('HiSPARC Lightning', 'HiSPARC Lightning Detector.exe')
    stop_executable('MySQL', 'mysqld.exe')
    stop_executable('HiSPARC Monitor', 'HiSPARC Monitor', cmd=True)
    stop_executable('HiSPARC Updater', 'HiSPARC Updater', cmd=True)


if __name__ == "__main__":
    startstop_logger.setup()
    stop_executables()
