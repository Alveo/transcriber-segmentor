import os
import shutil
import urllib.request
import urllib.error
import urllib.parse

from application import app

class URLDownloader:
    def __init__(self, url):
        self.url = url
        
        self.validURL = False
        self.alveoURL = False

        self._validateURL()

    def _validateURL(self):
        """ Validates whether the URL is both valid and whether it is a URL that needs an API library to access. Should not be called from outside the class. """
        schema = urllib.parse.urlparse(self.url)

        self.validURL = False
        self.alveoURL = False

        if schema.scheme is not '' and schema.netloc is not '':
            self.validURL = True

        if schema.netloc in app.config['ALVEO_DOMAINS']:
            self.alveoURL = True

    def isValid(self):
        """ Returns true if the URL protocol and address is valid. """
        return self.validURL

    def isAlveo(self):
        """ Returns true if the address matches an Alveo domain. """
        return self.alveoURL

    def _validate_path(self, filename):
        directory = os.path.dirname(os.path.realpath(filename))
        if not os.path.exists(directory):
            os.makedirs(directory)

    def download(self, filename):
        """ Downloads a file from the specified URL to the specified destination.

        Returns a HTTP status code. If it is not 200, it would be a safe assumption to say the download failed. """
        exit_code = 200

        self._validate_path(filename)

        try:
            with urllib.request.urlopen(self.url) as response, open(filename, 'wb') as file_handle:
                shutil.copyfileobj(response, file_handle)
        except urllib.error.HTTPError as exception:
            exit_code = exception.code

        return exit_code
