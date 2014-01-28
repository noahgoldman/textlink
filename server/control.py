import argparse

def runserver():
    from textlink import app
    app.run(debug=True)
    print "wat"

def get_arguments():
    parser = argparse.ArgumentParser(
            description="Various server control functions")

    subparsers = parser.add_subparsers(title='subcommands',
            description='valid subcommands')

    runserver_parser = subparsers.add_parser("runserver")
    runserver_parser.set_defaults(func=runserver)
    args = parser.parse_args()
    args.func()

if __name__ == '__main__':
    get_arguments()
