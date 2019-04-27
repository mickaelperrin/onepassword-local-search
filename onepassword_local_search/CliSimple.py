from .__version__ import __version__
from sys import exit
from onepassword_local_search.exceptions.ManagedException import ManagedException
from onepassword_local_search.OnePassword import OnePassword
from argparse import ArgumentParser


class CliSimple:

    action: str
    args: []
    field: str
    format: str
    script_name: str
    uuid: str

    def __init__(self, script_name, action='version', *args):

        self.parser = ArgumentParser()
        self.action = action
        self.script_name = script_name
        self.args = args

    def run(self):
        if self.action == 'get':
            return self.get()
        elif self.action == 'list':
            return self.list()
        else:
            return self.version()

    @staticmethod
    def usage(action='get'):
        if action == 'get':
            print('Usage: get field UUID')

    def get(self):
        self.parser.add_argument('uuid', help='uuid to fetch')
        self.parser.add_argument('field', help='field to retrieve')
        parsed_args = self.parser.parse_args(self.args)
        if parsed_args.uuid is None:
            print('Error: UUID is required to get secret')
            print(self.usage())
            exit(1)
        try:
            app = OnePassword()
            return app.get(parsed_args)
        except ManagedException as e:
            exit(e.args[0])

    def list(self):
        self.parser.add_argument('--format', help='custom format string')
        parsed_args = self.parser.parse_args(self.args)
        app = OnePassword()
        return app.list(parsed_args)

    @staticmethod
    def version():
        print('Version: ' + __version__)
