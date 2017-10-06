import os
from flask import Flask

app = Flask(__name__)
BASE_FOLDER = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
app.static_folder = os.path.join(BASE_FOLDER, 'static')
app.config.from_pyfile('../config')

# Allow cross origin headers only on dev mode
if app.config['DEVELOPMENT'] == True:
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

import application.routes
