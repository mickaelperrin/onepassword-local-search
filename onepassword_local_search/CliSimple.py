from .__version__ import __version__
from sys import exit
from onepassword_local_search.exceptions.ManagedException import ManagedException
from onepassword_local_search.OnePassword import OnePassword


class CliSimple:

    action: str
    args: []
    field: str
    format: str
    script_name: str
    uuid: str

    def __init__(self, script_name, action='version', *args):

        self.action = action
        self.script_name = script_name
        self.args = args

    def run(self):
        if self.action == 'get':
            if len(self.args) > 0:
                self.uuid = self.args[0]
            if len(self.args) > 1:
                self.field = self.args[1]
            if self.uuid is None:
                print('Error: UUID is required to get secret')
                print(self.usage())
                exit(1)
            return self.get(self.uuid, self.field)
        elif self.action == 'list':
            return self.list(self.args)
        else:
            return self.version()

    @staticmethod
    def usage(action='get'):
        if action == 'get':
            print('Usage: get field UUID')

    @staticmethod
    def get(uuid, field):
        try:
            app = OnePassword()
            return app.get(uuid, field)
        except ManagedException as e:
            exit(e.args[0])

    @staticmethod
    def list(args):
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('--format', help='custom format string')
        parsed_args = parser.parse_args(args)
        app = OnePassword()
        return app.list(parsed_args)

    @staticmethod
    def version():
        print('Version: ' + __version__)
