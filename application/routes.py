import uuid
from flask import jsonify, request

from application import app
from application.modules.route_post import segment_upload
from application.modules.route_url import segment_url

def not_allowed(error):
    """ 403 handler """
    return "403"

def not_found(error):
    """ 404 handler """
    return "404"

def server_error(error):
    """ 500 handler """
    return "500"

app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

app.add_url_rule('/api/segment/url', 'url', segment_url)
if app.config['ALLOW_FILE_POST']:
    app.add_url_rule('/api/segment/upload', 'upload', segment_upload, methods=['POST'])
