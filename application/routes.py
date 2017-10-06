import os
import uuid
from flask import redirect, jsonify, request

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

@app.before_first_request
def init():
    pass

@app.route('/')
def serve():
    return "Index"

@app.route('/api/segment/url')
def segment_url():
    status = ""
    url = request.args.get('url', default="", type=str)

    filename = app.config['DOWNLOAD_CACHE_PATH'] + str(uuid.uuid4())
    downloader = URLDownloader(url, filename)

    if downloader.isValid():
        status = downloader.download();

        # Confirm the file type is audio
        if status == 200:
            processor = AudioSegmentor(filename)
            if processor.isValid():
                status = jsonify(processor.segment())
            else: 
                status = "{error: \"Specified URL did not contain a valid .wav audio file.\"}"
        else:
            status = "{error: \"Resource returned error code "+str(status)+"\".}"
    else:
        status = "{error: \"URL pattern is not valid. Example: http://example.com/\"}"

    if status is "":
        status = "An unknown error occurred."

    downloader.cleanup()

    return status

@app.route('/api/segment/upload', methods=['POST'])
def segment_upload():
    status = ""
    if 'file' in request.files:
        filedata = request.files['file']
        if filedata.filename is not "":
            filename = app.config['DOWNLOAD_CACHE_PATH'] + str(uuid.uuid4())

            downloader = PostDownloader(filename, filedata)
            downloader.save()

            processor = AudioSegmentor(filename)
            if processor.isValid():
                status = jsonify(processor.segment())
            else: 
                status = "{error: \"Uploaded file is not a valid .wav audio file.\"}"
        else:
            status = "{error: \"No file selected in query.\"}"
    else:
        status = "{error: \"No file attached to query.\"}"

    if status is "":
        status = "An unknown error occurred."

    downloader.cleanup()

    return status
