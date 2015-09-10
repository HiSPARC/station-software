import os
import logging
import time
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('startstop')


def setup():
    """Setup for the startstop logger

    This configures the startstop logger, adding the handlers and
    setting the log levels.

    """
    logger.setLevel(level=logging.DEBUG)

    # Make sure the directory exists
    LOG_DIRNAME = '../../persistent/logs/startstop/'
    if not os.access(LOG_DIRNAME, os.F_OK):
        os.makedirs(LOG_DIRNAME)
    LOG_FILENAME = os.path.join(LOG_DIRNAME, 'startstop')

    # Remove any existing handlers
    logger.handlers = []

    # Use UTC time
    logging.Formatter.converter = time.gmtime

    # Add file handler
    handler = TimedRotatingFileHandler(LOG_FILENAME, when='midnight',
                                       backupCount=14, utc=True)
    handler.setLevel(level=logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)s.%(funcName)s.'
                                           '%(levelname)s: %(message)s',
                                           '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)

    # Add handler which prints to the screen
    handler = logging.StreamHandler()
    handler.setLevel(level=logging.INFO)
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
