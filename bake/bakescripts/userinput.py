#########################################################################################
#
# HiSPARC Installer Creator
# Code to create the HiSPARC installer
# Called from:  - bake.py
# Calls:        - none
#
# R.Hart@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# What this code does:
# - Accept user input
#
#########################################################################################
#
#     2013: - HiSPARC Installer Creator version 1.0
# Jul 2017: - HiSPARC Installer Creator version 2.0
#
#########################################################################################
class userInput(object):

    def __init__(self):
        pass

    def get_version(self, type):
        version = ""
        while (version == ""):
            version = raw_input("Which %s software version do you wish to "
                                "create? \n" % type)
        return version
