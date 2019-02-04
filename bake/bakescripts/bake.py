#########################################################################################
#
# HiSPARC Installer Creator
# Code to create the HiSPARC installer
# Called from:  - ../bake.bat
# Calls:        - nsis.py
#               - userinput.py
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this code does:
# - Check existence of directories
# - Asks user to define installer version
# - Compiles admininstaller.nsi
# - Compiles userunpacker.nsi
# - Compiles hisparcinstaller.nsi (maininstaller)
#
#########################################################################################
#
#     2013: - HiSPARC Installer Creator version 1.0
# Jul 2017: - HiSPARC Installer Creator version 2.0
#           - NSIS 3.02
#           - Introduction of installer creator version number (major/minor)
#
#########################################################################################

import os
import sys
from datetime import datetime

from userinput import userInput
from nsis import nsiHandling

# Files created will always be put in the "/bake/releases" directory
RELEASE_DIRECTORY = "./releases"

# Get HiSPARC Installer Version Numbers (admin, user and release numbers)
input = userInput()
nsiHandling = nsiHandling()

# Version 2.0 of the installer creator
print "\nWelcome to the HiSPARC Installer Creator Version 2.0!\n"
admin_version = input.get_version("administrator")
user_version = input.get_version("user")
release_number = input.get_version("release")

now = datetime.now()
release_date = now.strftime('%Y%m%d_%H%M%S')

# Check if the RELEASE_DIRECTORY exists, if not create
if not os.access(RELEASE_DIRECTORY, os.F_OK):
    os.makedirs(RELEASE_DIRECTORY)

# Compile the administrator software first
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

# Compile the user software
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

# Compile the main installer
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
