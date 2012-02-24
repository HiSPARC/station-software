# bake.py
# Create the HiSPARC installer.

from   userinput import *
from   nsis      import *
import os.path
import sys

#files created will always be put in the "\bake\releases" directory
RELEASE_DIRECTORY = "releases"

input = userInput()
nsiHandling = nsiHandling()

print "\nWelcome to the HiSPARC bake script!\n"
adminVersion = input.getVersion("administrator")
userVersion  = input.getVersion("user")

#compile the administrator software first
if os.path.exists('%s\\adminUpdater_v%s.exe' % (RELEASE_DIRECTORY, adminVersion)):
	print "Administrator installer already exists, not creating a new one!"
else:
	try: 
		nsiHandling.compileNSI("nsisscripts\\adminupdater\\admininstaller.nsi",
		["ADMIN_VERSION=%s" % adminVersion])
	except:
		print "ERROR: Compilation could not be finished!"
		sys.exit

#compile the user software second
if os.path.exists('%s\\userUnpacker_v%s.exe' % (RELEASE_DIRECTORY, userVersion)):
	print "User unpacker already exists, not creating a new one!"
else:
	try:
		nsiHandling.compileNSI("nsisscripts\\userunpacker\\userunpacker.nsi",
		["USER_VERSION=%s" % userVersion])
	except:
		print "ERROR: Compilation could not be finished!"
		sys.exit

#compile the main installer
try:
	nsiHandling.compileNSI("nsisscripts\\maininstaller\\hisparcinstaller.nsi",
	["ADMIN_VERSION=%s" % adminVersion]+["USER_VERSION=%s" % userVersion])
except:
	print "ERROR: Compilation could not be finished!"
	sys.exit

print "\nFinished compilation of version %s.%s.\n" % (adminVersion, userVersion)