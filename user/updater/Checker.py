import os
import ConfigParser
import checkFiles
import urllib2
import logging
from urlparse import parse_qs
from Tkinter import Message, Tk

from Downloader import Downloader

CONFIG_INI = "config.ini"
PERSISTENT_INI = "../../persistent/configuration/config.ini"
DISPLAY_GUI_MESSAGES = True
UPDATE_USER_MODE = 1
UPDATE_ADMIN_MODE = 2

logger = logging.getLogger('updater.checker')


class Checker(object):

    """Check for updates"""

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read([CONFIG_INI, PERSISTENT_INI])

    def requestCheckFromServer(self):
        server = self.config.get("Update", "UpdateURL")
        currentAdmin = self.config.get("Version", "CurrentAdmin")
        currentUser = self.config.get("Version", "CurrentUser")

        connection = urllib2.urlopen("%s/%s/%s" % (server, currentAdmin,
                                                   currentUser))
        updateInfo = connection.read()
        connection.close()
        return updateInfo

    def parseAnswerServer(self, updateInfo):
        updateDict = parse_qs(updateInfo, strict_parsing=True)
        # updateDict has: mustUpdate, urlUser, newVersionUser, urlAdmin,
        #                 newVersionAdmin
        updates = dict()  # updates has: mustUpdate, userFile, adminFile

        mustUpdate = int(updateDict['mustUpdate'][0])
        updates['mustUpdate'] = mustUpdate

        downloader = Downloader()
        location = "../../persistent/downloads"

        if mustUpdate == 0:
            logger.info('No update available')
        elif (mustUpdate & UPDATE_ADMIN_MODE):
            adminURL = updateDict['urlAdmin'][0]
            logger.info('Downloading Admin update: %s' % adminURL)
            adminFile = downloader.downloadUpdate(location, adminURL)
            updates['adminFile'] = adminFile
            logger.info('Administrator update is available called: %s' %
                        adminFile)

            if DISPLAY_GUI_MESSAGES and not(checkFiles.checkIfAdmin()):
                root = Tk()
                root.title('HiSPARC')
                Message(root, anchor='s', text="Update is available requiring "
                        "administrator rights!\nPlease ask your administrator "
                        "to reboot and install it!").pack(padx=150, pady=100)
                root.mainloop()

        elif (mustUpdate & UPDATE_USER_MODE):
            userURL = updateDict['urlUser'][0]
            logger.info('Downloading User update: %s' % userURL)
            userFile = downloader.downloadUpdate(location, userURL)
            updates['userFile'] = userFile
            logger.info('User update is available called: %s' % userFile)
            # Run the update to install it.
            # First call a batch file so that Python can be closed.
            os.system(".\\runUserUpdate.bat %s" % userFile)

        return updates

    def checkForUpdates(self):
        try:
            updateInfo = self.requestCheckFromServer()
        except:
            logger.exception('Could not reach server to check for updates.')
            return
        try:
            updates = self.parseAnswerServer(updateInfo)
        except:
            logger.exception('Could not parse answer of the server correctly.')
            return
        return updates
