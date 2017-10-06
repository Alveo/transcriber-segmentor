import uuid
from flask import jsonify, request

from application import app
from application.modules.downloader_url import URLDownloader
from application.modules.downloader_post import PostDownloader
from application.modules.audio_segment import AudioSegmentor

def not_allowed(error):
    """ 403 handler """
    return "403"

def not_found(error):
    """ 404 handler """
    return "404"

def server_error(error):
    """ 500 handler """
    return "500"

@app.route('/api/segment/url')
def segment_url():
    """ Segments a file via a specified url argument. Returns JSON if successful, else redirects an error message received from the resource. """

    status = ""
    url = request.args.get('url', default="", type=str)

    filename = app.config['DOWNLOAD_CACHE_PATH'] + str(uuid.uuid4())
    downloader = URLDownloader(url, filename)

    if downloader.isValid():
        # Try download the file from the specified resource
        status = downloader.download();

        if status == 200:
            # Attempt to segment the file
            processor = AudioSegmentor(filename)
            if processor.isValid():
                # Return pure JSON to the client
                status = jsonify(processor.segment())
            else: 
                status = "{error: \"Specified URL did not contain a valid .wav audio file.\"}"
        else:
            status = "{error: \"Resource returned error code "+str(status)+"\".}"
    else:
        status = "{error: \"URL pattern is not valid. Example: http://example.com/\"}"

    if status is "":
        status = "{error: \"An unknown error occurred.\"}"

    downloader.cleanup()
    return status

@app.route('/api/segment/upload', methods=['POST'])
def segment_upload():
    """ Segments a file receied via POST from a client. Returns JSON if successful, else an error message. """

    status = ""
    if 'file' in request.files:
        filedata = request.files['file']
        if filedata.filename is not "":
            filename = app.config['DOWNLOAD_CACHE_PATH'] + str(uuid.uuid4())

            # Save the file for audiosegmentor
            downloader = PostDownloader(filename, filedata)
            downloader.save()

            # Attempt to segment the file
            processor = AudioSegmentor(filename)
            if processor.isValid():
                # Return pure JSON to the client
                status = jsonify(processor.segment())
            else: 
                status = "{error: \"Uploaded file is not a valid .wav audio file.\"}"
        else:
            status = "{error: \"No file selected in query.\"}"
    else:
        status = "{error: \"No file attached to query.\"}"

    if status is "":
        status = "{error: \"An unknown error occurred.\"}"

    downloader.cleanup()
    return status
