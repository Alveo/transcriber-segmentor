from subprocess import Popen, PIPE, STDOUT

import json
from flask import redirect

from application import app
from application.modules.error_views import not_allowed, not_found, server_error

app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

@app.before_first_request
def init():
    pass

@app.route('/')
def serve():
    return "Index"

@app.route('/api/segment')
def segment():
    # TODO accept a URL
    # TODO download from URL
    # TODO return file as JSON
    wave_file = './static/test.wav'

    command = '%s/ssad -m 1.0 -a -s -f %s %s -'
    exe_cmd = command%('/home/audioseg/audioseg-1.2.2/src/', "16000.0", wave_file)

    p=Popen(['/home/audioseg/audioseg-1.2.2/src/ssad',
            '-m 1.0', '-a', '-s', '-f', '16000.0', wave_file, '-'],
            stdin=PIPE, stdout=PIPE, stderr=STDOUT);
    output = p.communicate()[0]

    return output
