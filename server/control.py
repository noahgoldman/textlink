import argparse

def runserver():
    from textlink import app
    app.run(debug=True)

def create_db():
    from textlink import Base, engine
    from textlink.models import *
    Base.metadata.create_all(bind=engine)

def get_arguments():
    parser = argparse.ArgumentParser(
            description="Various server control functions")

    subparsers = parser.add_subparsers(title='subcommands',
            description='valid subcommands')

    runserver_parser = subparsers.add_parser("runserver")
    runserver_parser.set_defaults(func=runserver)

    createdb_parser = subparsers.add_parser("createdb")
    createdb_parser.set_defaults(func=create_db)

    args = parser.parse_args()
    args.func()

if __name__ == '__main__':
    get_arguments()
