import uuid
from flask import jsonify, request

from application import app
from application.modules.downloader_url import URLDownloader
from application.modules.audio_segment import AudioSegmentor

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
        status = "{error: \"URL pattern is either not valid or not allowed. Example: http://example.com/\"}"

    if status is "":
        status = "{error: \"An unknown error occurred.\"}"

    downloader.cleanup()
    return status
