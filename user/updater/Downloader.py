from urllib import urlretrieve
import re
import checkFiles
import logging


logger = logging.getLogger('updater.downloader')


class Downloader(object):

    """Download available updates"""

    def downloadUpdate(self, location, URL):
        """Download an update

        :param location: local path where to store the downloaded update.
        :param URL: the url to download.

        """
        m = re.search('\/([^\/]*)\/?$', URL)
        if m:
            fileName = m.group(1)
        else:
            logger.error('URL to download is not valid')
            return 'NULL'
        if (location[-1] == '/') | (location[-1] == '^\\'):
            fileLocation = '%s%s' % (location, fileName)
        else:
            fileLocation = '%s/%s' % (location, fileName)
        if not checkFiles.checkIfEqualFileExists(location, fileName):
            urlretrieve(URL, fileLocation)
            logger.info('File downloaded!')
        else:
            logger.error('File already exist!')
        return fileLocation
