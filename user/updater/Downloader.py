from urllib import urlretrieve
import re
import checkFiles

from hslog import log


class Downloader(object):
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
