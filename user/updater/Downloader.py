from urllib import urlretrieve
import re
import checkFiles

from hslog import log


class Downloader():
    def downloadUpdate(self, location, URL):
        m = re.search('\/([^\/]*)\/?$', URL)
        if m:
            fileName = m.group(1)
        else:
            log('URL to download is not valid')
            return 'NULL'
        if (location[-1] == '/') | (location[-1] == '^\\'):
            fileLocation = '%s%s' % (location, fileName)
        else:
            fileLocation = '%s/%s' % (location, fileName)
        if not(checkFiles.checkIfEqualFileExists(location, fileName)):
            urlretrieve(URL, fileLocation)
            log('File downloaded!')
        else:
            log('File already exist!')
        return fileLocation

#Main function:
#ADL: This links to an old version?
#URL = ('http://www.hisparc.nl/drupal/files/'
#       'HiSPARC%20Software%20Installatie%20V1-0.pdf')

#downloader = Downloader()
#downloadLocation = downloader.config.get('UpdateLocation', 'AdminLocation')

#location = downloader.downloadUpdate(downloadLocation, URL)
