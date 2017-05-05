import os

from app.cli.application import CLI

if __name__ == '__main__':
    cli = CLI(os.getcwd() + '/storage.json')
    cli.run()
