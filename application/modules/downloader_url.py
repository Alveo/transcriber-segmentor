import shutil
import urllib.request
import urllib.error
import urllib.parse

def isValid(url):
    valid = False

    schema = urllib.parse.urlparse(url)

    if schema.scheme != '' and schema.netloc != '':
        valid = True

    return valid

def download(url, filename):
    """ Downloads a file from the specified URL to the specified destination.

    Returns a HTTP status code. If it is not 200, it would be a safe assumption to say the download failed. """
    exit_code = 200

    try:
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as file_handle:
            shutil.copyfileobj(response, file_handle)
    except urllib.error.HTTPError as exception:
        exit_code = exception.code

    return exit_code
