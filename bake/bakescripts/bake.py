# bake.py
# Create the HiSPARC installer.

import os
import sys

from userinput import *
from nsis      import *

#files created will always be put in the "\bake\releases" directory
RELEASE_DIRECTORY = "./releases"

input = userInput()
nsiHandling = nsiHandling()

print "\nWelcome to the HiSPARC bake script!\n"
adminVersion = input.getVersion("administrator")
userVersion  = input.getVersion("user")

#check if the RELEASE_DIRECTORY exists, if not create it
if not os.access(RELEASE_DIRECTORY, os.F_OK):
    os.makedirs(RELEASE_DIRECTORY)

#compile the administrator software first
if os.path.exists("%s/adminUpdater_v%s.exe" % (RELEASE_DIRECTORY, adminVersion)):
    print "Administrator installer already exists, not creating a new one!"
else:
    try:
        nsiHandling.compileNSI("./nsisscripts/adminupdater/admininstaller.nsi",
        ["ADMIN_VERSION=%s" % adminVersion])
    except:
        print "ERROR: Compilation could not be finished!"
        sys.exit

#compile the user software second
if os.path.exists("%s/userUnpacker_v%s.exe" % (RELEASE_DIRECTORY, userVersion)):
    print "User unpacker already exists, not creating a new one!"
else:
    try:
        nsiHandling.compileNSI("./nsisscripts/userunpacker/userunpacker.nsi",
        ["USER_VERSION=%s" % userVersion])
    except:
        print "ERROR: Compilation could not be finished!"
        sys.exit

#compile the main installer
try:
    nsiHandling.compileNSI("./nsisscripts/maininstaller/hisparcinstaller.nsi",
    ["ADMIN_VERSION=%s" % adminVersion]+["USER_VERSION=%s" % userVersion])
except:
    print "ERROR: Compilation could not be finished!"
    sys.exit

print "\nFinished compilation of version %s.%s.\n" % (adminVersion, userVersion)
