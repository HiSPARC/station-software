import logging
from ConfigParser import ConfigParser

logger = logging.getLogger('hsmonitor.econfigparser')


class EConfigParser(ConfigParser):

    """Extend the Config parser to make parsing easier"""

    def ifget(self, section, option, dtype, default):
        if self.has_option(section, option):
            try:
                return dtype(self.get(section, option))
            except ValueError:
                logger.warning('Unable to parse option %s.%s, '
                               'using default: %s' %
                               (section, option, str(default)))
                return default
        else:
            logger.warning('Option %s.%s not specified, using default: %s' %
                           (section, option, str(default)))
            return default

    def ifgetint(self, section, option, default):
        return self.ifget(section, option, int, default)

    def ifgetstr(self, section, option, default):
        return self.ifget(section, option, str, default)

    def ifgetfloat(self, section, option, default):
        return self.ifget(section, option, float, default)

    def itemsdict(self, section):
        # convert a config list to dictionary variable
        # (need to use small letters in the names)
        result = {}
        for key, value in self.items(section):
            result[key] = value
        return result
