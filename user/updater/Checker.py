import ConfigParser
from urllib import urlencode
import urllib2
from cgi import parse_qs
import sys
from Downloader import Downloader
from Tkinter import *
from hslog import *
import checkFiles

PERSISTENT_INI = '/persistent/configuration/config.ini'
CONFIG_INI = 'config.ini'
DISPLAY_GUI_MESSAGES = True

class OurOpener(urllib2.OpenerDirector):
    pass

class Checker:
    #Internal handle to the database cursor
    config = ConfigParser.ConfigParser()
    dbHandle = 0
    UPDATE_USER_MODE = 1
    UPDATE_ADMIN_MODE = 2

    def __init__(self):
        self.config.read([CONFIG_INI, PERSISTENT_INI])
        
    def requestCheckFromServer(self):
        server = self.config.get('Update', 'UpdateURL')
        stationname = self.config.get('Station', 'Nummer')
        currentUser = self.config.get('Version', 'CurrentUser')
        currentAdmin = self.config.get('Version', 'CurrentAdmin')
        intervalBetweenChecks = self.config.get('Update',
                                                'IntervalBetweenChecks')
        params = urlencode({'admin_version': currentAdmin,
                            'user_version': currentUser,
                            'station_id': stationname})

        #urllib2.urlopen('%s?%s' % (server, params))

        updateInfo = ''
        proxy_support = urllib2.ProxyHandler()
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='HiSPARC restricted',
                                  uri=server,
                                  user='dummy',
                                  passwd='dummy')
        opener = urllib2.build_opener(auth_handler, proxy_support)
        # ...and install it globally so it can be used with urlopen.
        urllib2.install_opener(opener)     
        url = '%s?%s' % (server, params)
        connection = urllib2.urlopen(url)
        updateInfo = connection.read()
        print updateInfo
        connection.close()
            
        #except (urllib2.URLError, urllib2.HTTPError), msg:
        #    # For example: connection refused or internal server error
        #    returncode = str(msg)
        #except Exception, msg:
        #    returncode = 'Uncatched exception occured in function ' \
        #                 'upload_event_list: %s' % str(msg)
        
        return updateInfo

    def parseAnswerServer(self, updateInfo):
        updateDict = parse_qs(updateInfo, strict_parsing=True)
        #updateDict has: mustUpdate, urlUser, newVersionUser, urlAdmin, newVersionAdmin
        downloader = Downloader()
        updates = dict() #updates has: mustUpdate, userFile, adminFile
        
        mustUpdate = int(updateDict['mustUpdate'][0])
        updates['mustUpdate'] = mustUpdate
        
        virtualDrive = self.config.get('Station', 'VirtualDrive')
        location = "%s:/persistent/downloads" % virtualDrive

        if (mustUpdate & self.UPDATE_ADMIN_MODE):
            adminURL = updateDict['urlAdmin'][0]
            print adminURL
            adminFile = downloader.downloadUpdate(location, adminURL)
            updates['adminFile'] = adminFile
            log('Administrator update is available called: %s' % adminFile)
            
            if DISPLAY_GUI_MESSAGES and not(checkFiles.checkIfAdmin()):
                root = Tk()
                root.title('HiSparc')
                Message(root, anchor='s', text="Update is available requiring "
                        "administrator rights!\nPlease ask your administrator "
                        "to reboot and install it!").pack(padx=150, pady=100)
                root.mainloop()

        elif (mustUpdate & self.UPDATE_USER_MODE):
            userURL = updateDict['urlUser'][0]
            userFile = downloader.downloadUpdate(location, userURL)
            updates['userFile'] = userFile
            log('User update is available called: %s' % userFile)
            #Run the update to install it.
            #first call a batch file so that Python can be closed. 
            os.system('/user/updater/runUserUpdate.bat %s' % userFile)

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

#Main function
#checker = Checker()
#updateInfo = checker.requestCheckFromServer()
#updates = checker.parseAnswerServer(updateInfo)
