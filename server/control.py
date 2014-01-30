import argparse

def runserver():
    from textlink import app
    app.run(debug=True)

def create_db():
    from textlink import Base, engine
    from textlink.models import Number, Phone, List
    Base.metadata.create_all(bind=engine)

def shell():
    import readline
    import code

    var = globals().copy()
    var.update(locals())
    shell = code.InteractiveConsole(var)
    shell.push("from textlink import app, Session")
    shell.push("from textlink.models import Number, Phone, List")
    shell.push("session = Session()")
    shell.interact()

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

    args = parser.parse_args()
    args.func()

if __name__ == '__main__':
    get_arguments()
