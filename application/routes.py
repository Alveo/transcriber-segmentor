import os
import uuid
from flask import redirect, jsonify, request

from application import app
from application.modules.error_views import not_allowed, not_found, server_error
from application.modules.downloader_url import URLDownloader
from application.modules.audio_segment import AudioSegmentor

app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

@app.before_first_request
def init():
    pass

@app.route('/')
def serve():
    return "Index"

@app.route('/api/segment/url')
def url_download():
    status = "An unknown error occurred."

    url = request.args.get('url', default="", type=str)

    filename = app.config['DOWNLOAD_CACHE_PATH'] + str(uuid.uuid4())
    downloader = URLDownloader(url, filename)

    if downloader.isValid():
        if not downloader.isAlveo():
            status = downloader.download();

            # Confirm the file type is audio
            if status == 200:
                processor = AudioSegmentor(filename)
                if processor.isValid():
                    status = jsonify(processor.segment())

                status = "{error: \"Specified URL did not contain a valid .wav audio file.\"}"
            else:
                status = "{error: \"Resource returned error code "+str(status)+"\".}"
        else:
            status = "{error: \"Alveo URLs are currently not supported.\"}"
    else:
        status = "{error: \"URL pattern is not valid. Example: http://example.com/\"}"

    downloader.cleanup()
    return status
