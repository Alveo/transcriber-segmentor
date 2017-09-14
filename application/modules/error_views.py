from flask import redirect

from application import app

# 403 handler
def not_allowed(error):
    return "403"

# 404 handler
def not_found(error):
    return "404"

# 500 handler
def server_error(error):
    return "500"
