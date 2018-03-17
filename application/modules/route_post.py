import uuid
from flask import jsonify, request

from application import app
from application.modules.downloader_post import PostDownloader
from application.modules.audio_segment import AudioSegmentor
from application.modules.api_error import api_error

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
                status = api_error("Uploaded file is not a valid .wav audio file.")

            downloader.cleanup()
        else:
            status = api_error("No file selected in query.")
    else:
        status = api_error("No file attached to query.")

    if status is "": # Catch any unexpected responses
        status = api_error("An unknown error occurred.")

    return status
