import os
import shutil
import urllib.request
import urllib.error
import urllib.parse

import pyalveo

from application import app

class URLDownloader:
    """ URLDownloader is a class for managing the process of validating, downloading and cleaning up a file.

        Supports the Alveo service for AusTalk data. """

    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        
        self.downloaded = False
        self.validURL = False
        self.alveoURL = False

        self._validateURL()

    def _validateURL(self):
        """ Validates whether the URL is both valid and whether it is a URL that needs an API library to access. Should not be called from outside the class. """
        schema = urllib.parse.urlparse(self.url)

        self.validURL = False
        self.alveoURL = False

        if schema.scheme is not '':
            if schema.netloc in app.config['ALVEO_DOMAINS']:
                self.alveoURL = True
                self.validURL = True
            elif schema.netloc is not '' and app.config['ALLOW_GENERIC_URL']:
                self.validURL = True

    def _validate_path(self):
        """ Validates whether the directory exists or not. Creates the directory if it does not exist. Should not be called from outside the class. """
        directory = os.path.dirname(os.path.realpath(self.filename))
        if not os.path.exists(directory):
            os.makedirs(directory)

    def isValid(self):
        """ Returns true if the URL protocol and address is valid. """
        return self.validURL

    def isAlveo(self):
        """ Returns true if the address matches an Alveo domain. """
        return self.alveoURL

    def download(self):
        """ Downloads a file from the specified URL to the specified destination.

        Returns a HTTP status code. If it is not 200, it would be a safe assumption to say the download failed. """
        exit_code = 200
        self._validate_path()

        if not self.isAlveo():
            exit_code = self._genericDownload();
            if exit_code is 200:
                self.downloaded = True
        else:
            exit_code = self._alveoDownload();

        return exit_code

    def _alveoDownload(self):
        """ Attempts to download via the Alveo service. """
        exit_code = 200

        # TODO Alveo exceptions
        client = pyalveo.Client(configfile=app.config['PYALVEO_CONFIG_PATH'], use_cache=True, cache_dir=app.config['PYALVEO_CACHE_DIR'])
        try:
            doc = client.get_document(self.url)

            f = open(self.filename, 'wb')
            f.write(doc)
            f.close()
        except pyalveo.pyalveo.APIError as e:
            exit_code = e.http_status_code
        except IOError as e:
            exit_code = 500

        return exit_code

    def _genericDownload(self):
        """ Attempts to download via a generic URL. """
        exit_code = 200

        try:
            with urllib.request.urlopen(self.url) as response, open(self.filename, 'wb') as file_handle:
                shutil.copyfileobj(response, file_handle)
        except urllib.error.HTTPError as exception:
            exit_code = exception.code
        except urllib.error.URLError as exception:
            exit_code = exception.reason
        except IOError as e:
            status = 500

        return exit_code

    def cleanup(self):
        """ Erases any downloaded data. """
        if self.downloaded:
            os.remove(self.filename)
            self.downloaded = False
