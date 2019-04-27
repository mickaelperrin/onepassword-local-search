from .__version__ import __version__
from sys import exit
from onepassword_local_search.exceptions.ManagedException import ManagedException
from onepassword_local_search.OnePassword import OnePassword
from argparse import ArgumentParser, Namespace


class CliSimple:

    args: Namespace
    command: str

    def __init__(self, *args):

        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')

        action_get = subparsers.add_parser('get')
        action_get.add_argument('uuid', help='uuid to fetch')
        action_get.add_argument('field', help='field to retrieve')
        action_get.add_argument('--use-custom-uuid', help='use custom UUID mapping')

        action_list = subparsers.add_parser('list')
        action_list.add_argument('--format', help='custom format string')

        action_version = subparsers.add_parser('version')

        action_update_mapping = subparsers.add_parser('update-mapping')

        self.args = parser.parse_args(args[1:])

    def run(self):
        return getattr(self, self.args.command.replace('-', '_'))()

    @staticmethod
    def usage(action='get'):
        if action == 'get':
            print('Usage: get field UUID')

    def get(self):
        try:
            app = OnePassword(self.args)
            return app.get(self.args)
        except ManagedException as e:
            exit(e.args[0])

    def list(self):
        app = OnePassword(self.args)
        return app.list()

    def update_mapping(self):
        app = OnePassword(self.args)
        return app.update_mapping()

    @staticmethod
    def version():
        print('Version: ' + __version__)
