import settings
from definitions import *

import logging
logger = logging.getLogger("diagnostics")


def run_checks():
    enabled_checks = []
    for check in settings.ENABLED_CHECKS:
        exec "import %s" % check
        enabled_checks.append(eval("%s.Check()" % check))

    for check in enabled_checks:
        logger.info(check.__doc__)
        check.run()
        logger.info(status.string(check.status))
        logger.info(check.message)

    logger.info(40 * '-')
    logger.info("Summary of the results:")
    logger.info(40 * '-')
    for check in enabled_checks:
        logger.info(str(check) + ': ' + status.string(check.status))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run_checks()
