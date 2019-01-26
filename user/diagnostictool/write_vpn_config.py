import os
import shutil
from datetime import datetime
import logging

from proxy_settings import Check

logger = logging.getLogger("write_vpn_config")


def write_config():
    proxy_settings = Check()
    proxy_settings.run()

    logger.debug("Updating both 32 and 64-bit config")
    dst_dirs = ['../../admin/openvpn/x64/config', '../../admin/openvpn/x32/config']
    config_name = 'hisparc.ovpn'
    for dst_dir in dst_dirs:
        config = os.path.join(dst_dir, config_name)
        bak_config = config + '.' + datetime.now().strftime("%Y%m%d-%H%M%S")
        logger.debug("Moving old config to %s" % bak_config)
        try:
            os.rename(config, bak_config)
        except OSError:
            logger.warning("Unable to backup old config. Does it exist?")
        logger.debug("Copying new config")
        shutil.copyfile(config_name, config)

        if proxy_settings.enabled:
            logger.info("Proxy enabled, adding proxy settings")
            server, port = proxy_settings.server.split(':')
            with open(config, 'a') as config_file:
                config_file.write('\n\n')
                config_file.write('http-proxy %s %s\n' % (server, port))
                config_file.write('http-proxy-retry\n')
        else:
            logger.info("No proxy enabled, using default config.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    write_config()
