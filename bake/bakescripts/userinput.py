class userInput():
	ADMIN = 0
	USER = 1
	
	def __init__(self):
		return
	
	def getVersion(self, type):
		version = ""
		while (version == ""):
			version = raw_input("What %s software version do you want to make? \n" % type)
		return version