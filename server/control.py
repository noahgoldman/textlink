import argparse
import os
from subprocess import call

from textlink import create_db

def runserver():
    from textlink import app
    app.run(debug=True)

def shell():
    import readline
    import code

    var = globals().copy()
    var.update(locals())
    shell = code.InteractiveConsole(var)
    shell.push("from textlink import app, Session")
    shell.push("from textlink.models import *")
    shell.push("session = Session()")
    shell.interact()

def test():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests')
    os.environ['TEXTLINK_CONFIG'] = 'TESTING'
    os.chdir(path)
    call("nosetests")

#---------------------
# Command Line parsing
#---------------------

def get_arguments():
    parser = argparse.ArgumentParser(
            description="Various server control functions")

    subparsers = parser.add_subparsers(title='subcommands',
            description='valid subcommands')

    runserver_parser = subparsers.add_parser("runserver")
    runserver_parser.set_defaults(func=runserver)

    createdb_parser = subparsers.add_parser("createdb")
    createdb_parser.set_defaults(func=create_db)

    shell_parser = subparsers.add_parser("shell")
    shell_parser.set_defaults(func=shell)

    shell_parser = subparsers.add_parser("test")
    shell_parser.set_defaults(func=test)

    args = parser.parse_args()
    args.func()

if __name__ == '__main__':
    get_arguments()
