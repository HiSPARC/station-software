import logging

import settings
from definitions import status

logger = logging.getLogger("diagnostics")

help_message = """Welcome to the HiSPARC Diagnostic Tool.

This tool is now performing some system checks and will display a summary at the
end of this screen. If you have any problems with the VPN connection, please
click on the `Write VPN config' button, reboot the computer and rerun this tool.

If you continue to have problems with any of these checks, please contact
HiSPARC at info@hisparc.nl. It will be helpful if you include the contents of
this screen (copy, paste should work for any decent mailer).

Please, refrain from embedding text or screenshots in Microsoft Word documents.
Simply including text and graphics inside your message or as an attachment will
enable us to more quickly assess the situation.

Thank you!

"""

def run_checks():
    logger.info(help_message)

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
