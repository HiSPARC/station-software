#########################################################################################
#
# HiSPARC Installer Creator
# Code to create the HiSPARC installer
# Called from:  - bake.py
# Calls:        - nsis compiler
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this code does:
# - Compile .nsi file
#
#########################################################################################
#
#     2013: - HiSPARC Installer Creator version 1.0
# Jul 2017: - HiSPARC Installer Creator version 2.0
#           - NSIS 3.01
#
#########################################################################################

import subprocess

# Set path for nsis directory
NSISPATH = "./nsis"


class nsiHandling(object):
# Compile nsis file
    def __init__(self):
        self.nsisExe = "%s/makensis.exe" % NSISPATH

    def compileNSI(self, nsiPath, defines):
        definelist = ""
        # print str(defines)
        for i in defines:
            definelist = "%s /D%s" % (definelist, i)
        # print definelist
        command = "%s /V1 %s %s" % (self.nsisExe, definelist, nsiPath)
        # print command
        print "Compiling %s..." % nsiPath
        nsiProcess = subprocess.Popen(command)
        nsiProcess.wait()
        print "Compilation of %s finished!" % nsiPath
