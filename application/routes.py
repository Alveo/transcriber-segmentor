from flask import jsonify

from application import app
from application.modules.route_post import segment_upload
from application.modules.route_url import segment_url

def url_error(error_code):
    response = jsonify({'error': True, 'code': error_code})
    response.status_code = error_code;
    return response

def not_allowed(error):
    return url_error(403)

def not_found(error):
    return url_error(404)

def server_error(error):
    return url_error(500)

app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

app.add_url_rule('/api/segment/url', 'url', segment_url)
if app.config['ALLOW_FILE_POST']:
    app.add_url_rule('/api/segment/upload', 'upload', segment_upload, methods=['POST'])
