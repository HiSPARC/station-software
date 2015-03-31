# bake.py
# Create the HiSPARC installer.

import os
import sys
from datetime import datetime

from userinput import userInput
from nsis import nsiHandling


# files created will always be put in the "/bake/releases" directory
RELEASE_DIRECTORY = "./releases"

input = userInput()
nsiHandling = nsiHandling()

print "\nWelcome to the HiSPARC bake script!\n"
admin_version = input.get_version("administrator")
user_version = input.get_version("user")
release_number = input.get_version("release")

now = datetime.now()
release_date = now.strftime('%Y%m%d_%H%M%S')

# check if the RELEASE_DIRECTORY exists, if not create it
if not os.access(RELEASE_DIRECTORY, os.F_OK):
    os.makedirs(RELEASE_DIRECTORY)

# compile the administrator software first
if os.path.exists("%s/adminUpdater_v%s.exe" % (RELEASE_DIRECTORY,
                                               admin_version)):
    print "Administrator installer already exists, not creating a new one!"
else:
    try:
        nsiHandling.compileNSI("./nsisscripts/adminupdater/admininstaller.nsi",
                               ["ADMIN_VERSION=%s" % admin_version])
    except:
        print "ERROR: Compilation could not be finished!"
        sys.exit

# compile the user software
if os.path.exists("%s/userUnpacker_v%s.exe" % (RELEASE_DIRECTORY,
                                               user_version)):
    print "User unpacker already exists, not creating a new one!"
else:
    try:
        nsiHandling.compileNSI("./nsisscripts/userunpacker/userunpacker.nsi",
                               ["USER_VERSION=%s" % user_version])
    except:
        print "ERROR: Compilation could not be finished!"
        sys.exit

# compile the main installer
try:
    nsiHandling.compileNSI("./nsisscripts/maininstaller/hisparcinstaller.nsi",
                           ["ADMIN_VERSION=%s" % admin_version] +
                           ["USER_VERSION=%s" % user_version] +
                           ["RELEASE=%s" % release_number] +
                           ["RELEASE_DATE=%s" % release_date])
except:
    print "ERROR: Compilation could not be finished!"
    sys.exit

print ("\nFinished compilation of version %s.%s.%s.\n" %
       (admin_version, user_version, release_number))
