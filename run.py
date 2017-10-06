import sys
""" Note that manage.py is used only as utility in production to run the server,
        Gunicorn is used instead so bytecode will be created as expected in
        production and testing environments. """
sys.dont_write_bytecode = True

from application import app

app.run(host='0.0.0.0')
