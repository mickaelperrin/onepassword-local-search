from sys import exit
from onepassword_local_search.exceptions.ManagedException import ManagedException
from onepassword_local_search.OnePassword import OnePassword
from argparse import ArgumentParser, Namespace
import sys


class CliSimple:

    args: Namespace
    command: str

    def __init__(self, *args):

        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')

        action_get = subparsers.add_parser('get')
        action_get.add_argument('uuid', help='uuid to fetch')
        action_get.add_argument('field', help='field to retrieve', nargs='?', default=None)
        action_get.add_argument('--use-custom-uuid', help='use custom UUID mapping', nargs='?', default=False, const=True)

        action_list = subparsers.add_parser('list')
        action_list.add_argument('--format', help='custom format string')
        action_list.add_argument('--filter', help='filter over title entry')

        action_is_authenticated = subparsers.add_parser('is-authenticated')

        action_version = subparsers.add_parser('version')

        action_update_mapping = subparsers.add_parser('mapping')
        action_update_mapping.add_argument('subcommand', help='update or list', choices=['list', 'update'])

        self.args = parser.parse_args(args[1:])

    def run(self):
        try:
            app = OnePassword(self.args)
            return getattr(app, self.args.command.replace('-', '_'))()
        except ManagedException as e:
            exit(e.args[0])
        except (BrokenPipeError, IOError):
            sys.stderr.close()
            pass



