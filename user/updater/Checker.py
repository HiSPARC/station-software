#
#   Checker.py ------
#
import os
import sys
import ConfigParser
import checkFiles
import urllib2

from cgi        import parse_qs
from Tkinter    import Message, Tk
from hslog      import log, SEVERITY_CRITICAL
from Downloader import Downloader

CONFIG_INI           = "config.ini"
PERSISTENT_INI       = "../../persistent/configuration/config.ini"
DISPLAY_GUI_MESSAGES = True
UPDATE_USER_MODE     = 1
UPDATE_ADMIN_MODE    = 2


class Checker:
    #Internal handle to the database cursor
    config = ConfigParser.ConfigParser()

    def __init__(self):
        self.config.read([CONFIG_INI, PERSISTENT_INI])

    def requestCheckFromServer(self):
        server       = self.config.get("Update",  "UpdateURL")
        currentAdmin = self.config.get("Version", "CurrentAdmin")
        currentUser  = self.config.get("Version", "CurrentUser")

        connection = urllib2.urlopen("%s/%s/%s" % (server, currentAdmin, currentUser))
        updateInfo = connection.read()
        print updateInfo
        connection.close()
        return updateInfo

    def parseAnswerServer(self, updateInfo):
        updateDict = parse_qs(updateInfo, strict_parsing=True)
        #updateDict has: mustUpdate, urlUser, newVersionUser, urlAdmin,
        #                newVersionAdmin
        downloader = Downloader()
        updates = dict()  # updates has: mustUpdate, userFile, adminFile

        mustUpdate = int(updateDict['mustUpdate'][0])
        updates['mustUpdate'] = mustUpdate

        location = "../../persistent/downloads"

        if (mustUpdate & UPDATE_ADMIN_MODE):
            adminURL = updateDict['urlAdmin'][0]
            print adminURL
            adminFile = downloader.downloadUpdate(location, adminURL)
            updates['adminFile'] = adminFile
            log('Administrator update is available called: %s' % adminFile)

            if DISPLAY_GUI_MESSAGES and not(checkFiles.checkIfAdmin()):
                root = Tk()
                root.title('HiSPARC')
                Message(root, anchor='s', text="Update is available requiring "
                        "administrator rights!\nPlease ask your administrator "
                        "to reboot and install it!").pack(padx=150, pady=100)
                root.mainloop()

        elif (mustUpdate & UPDATE_USER_MODE):
            userURL = updateDict['urlUser'][0]
            userFile = downloader.downloadUpdate(location, userURL)
            updates['userFile'] = userFile
            log('User update is available called: %s' % userFile)
            # Run the update to install it.
            # First call a batch file so that Python can be closed.
            os.system("./runUserUpdate.bat %s" % userFile)

        return updates

    def checkForUpdates(self):
        try:
            updateInfo = self.requestCheckFromServer()
        except:
            log('Could not reach the server to check for updates: : %s' %
                str(sys.exc_info()[1]), severity=SEVERITY_CRITICAL)
            return
        try:
            updates = self.parseAnswerServer(updateInfo)
            return updates
        except:
            log('Could not parse the answer of the server correctly: %s' %
                str(sys.exc_info()[1]), severity=SEVERITY_CRITICAL)
            return
