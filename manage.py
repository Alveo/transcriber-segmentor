import sys
""" Note that manage.py is used only as utility in production to run the server,
        Gunicorn is used instead so bytecode will be created as expected in
        production and testing environments. """
sys.dont_write_bytecode = True

from flask_script import Manager, Command

from application import app, db

def gen_sample():
    gen_blank()

    db.session.commit();

def gen_blank():
    db.drop_all();
    db.create_all();

    db.session.commit();

manager = Manager(app)
@manager.command
def gendb(type):
    if type == "sample":
        gen_sample()
        print('Debug: Sample database has been generated.')

    elif type == "blank":
        gen_blank()
        print('Debug: Blank database has been generated.')

    else:
        print("Error: unknown database type '"+type+"'")

@manager.command
def runserver(force=False):
    if app.config['DEBUG'] or force:
        app.run(host='0.0.0.0')
    else:
        print("Error: Configuration is not in debug mode and not expected to run through this interface. Please launch via Gunicorn instead or use the --force option.")

if __name__ == '__main__':
    manager.run()
