class userInput():
	
	def __init__(self):
		pass
	
	def getVersion(self, type):
		version = ""
		while (version == ""):
			version = raw_input("What %s software version do you want to make? \n" % type)
		return version