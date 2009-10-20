from ConfigParser import ConfigParser
import sys
sys.path.append("..\..\pythonshared")
import hslog

class EConfigParser(ConfigParser):
	# extend the Config parser to make parsing easier
	def __init__(self):
		ConfigParser.__init__(self)

	def ifget(self, section, option, type, default):
		if self.has_option(section, option):
			return type(self.get(section, option))
		else:
			hslog.log("ConfigParser: option %s.%s not specified, using default: %s" % (section, option, str(default)))
			return default

	def ifgetint(self, section, option, default):
		return self.ifget(section, option, int, default)

	def ifgetstr(self, section, option, default):
		return self.ifget(section, option, str, default)

	def ifgetfloat(self, section, option, default):
		return self.ifget(section, option, float, default)

	def itemsdict(self, section):
		# convert a config list to dictionary variable -> need to use small letters in the names
		result = {}
		for key, value in self.items(section):
			result[key] = value
		return result
