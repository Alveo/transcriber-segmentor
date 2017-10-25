#!env/bin/python
""" This file should only be used for development. Please run the application via Gunicorn for production purposes. """
import sys
sys.dont_write_bytecode = True

from application import app

app.run(host='0.0.0.0', port=8000)
