import subprocess

NSISPATH = "./nsis"

class nsiHandling():

	def __init__(self):
		self.nsisExe = "%s/makensis.exe" % NSISPATH

	def compileNSI(self, nsiPath, defines):
		definelist = ""
		#print str(defines)
		for i in defines:
			definelist = "%s /D%s" % (definelist, i)	
		#print definelist
		command = "%s /V1 %s %s" % (self.nsisExe, definelist, nsiPath)
		#print command
		print "Compiling %s..." % nsiPath
		nsiProcess = subprocess.Popen(command)
		nsiProcess.wait()
		print "Compilation of %s finished!" % nsiPath