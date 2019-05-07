from sys import exit
from onepassword_local_search.exceptions.Hook import exception_handler
from onepassword_local_search.exceptions.ManagedException import ManagedException
from onepassword_local_search.OnePassword import OnePassword
from argparse import ArgumentParser, Namespace
import sys
sys.excepthook = exception_handler


class CliSimple:

    onePassword: OnePassword
    args: Namespace
    command: str

    def __init__(self, *args):

        parser = ArgumentParser(prog='op-local', description='Performs get/list operations over the local 1Password database')
        parser.add_argument('--disable-session-caching', help='disable session caching. The session caching is required for multi accounts setups.', nargs='?', default=False,
                                const=True)
        subparsers = parser.add_subparsers(dest='command')

        action_get = subparsers.add_parser('get', help='retrieve a single field/object given a uuid')
        action_get.add_argument('uuid', help='uuid to fetch')
        action_get.add_argument('field', help='field to retrieve', nargs='?', default=None)
        action_get.add_argument('--use-custom-uuid', help='use custom UUID mapping', nargs='?', default=False, const=True)
        action_get.add_argument('--use-lastpass-uuid', help='use LastPass UUID mapping', nargs='?', default=False, const=True)

        action_list = subparsers.add_parser('list', help='list all available entries')
        action_list.add_argument('--format', help='custom format string')
        action_list.add_argument('--filter', help='filter over title entry')
        action_list.add_argument('--output-encoding', help='encode values in one of the supported format: (json)', default=None)

        action_is_authenticated = subparsers.add_parser('is-authenticated', help='check if authenticated locally')

        action_version = subparsers.add_parser('version')

        action_update_mapping = subparsers.add_parser('mapping', help='operations on uuid mapping')
        action_update_mapping.add_argument('subcommand', help='update or list', choices=['list', 'update'])
        action_update_mapping.add_argument('--use-lastpass-uuid', help='list using lastpass uuid', nargs='?', default=False, const=True)

        self.args = parser.parse_args(args[1:])

        if self.args.disable_session_caching:
            from onepassword_local_search.services.CryptoService import CryptoService
            CryptoService.cleanup_sessions_cache()

        if self.args.command is None:
            parser.print_help()

    def run(self):
        try:
            if self.args.command is None or self.args.command == 'version':
                return self.version()
            custom_uuid_mapping = None
            if hasattr(self.args, 'use_custom_uuid') and self.args.use_custom_uuid:
                custom_uuid_mapping = 'UUID'
            elif hasattr(self.args, 'use_lastpass_uuid') and self.args.use_lastpass_uuid:
                custom_uuid_mapping = 'LASTPASS'
            self.onePassword = OnePassword(custom_uuid_mapping=custom_uuid_mapping, disable_session_caching=self.args.disable_session_caching)
            return getattr(self, self.args.command.replace('-', '_'))()
        except ManagedException as e:
            print(e.args[0], file=sys.stderr)
            sys.exit(1)
        except (BrokenPipeError, IOError):
            sys.stderr.close()
            pass

    def get(self):
        if self.args.use_custom_uuid:
            custom_uuid_mapping = 'UUID'
        elif self.args.use_lastpass_uuid:
            custom_uuid_mapping = 'LASTPASS'
        else:
            custom_uuid_mapping = None
        return self.onePassword.get(self.args.uuid, self.args.field, custom_uuid_mapping)

    def list(self):
        return self.onePassword.list(self.args.format, self.args.filter, result_encoding=self.args.output_encoding)

    def mapping(self):
        return self.onePassword.mapping(self.args.subcommand, self.args.use_lastpass_uuid)

    def version(self):
        return OnePassword.version()

    def is_authenticated(self):
        if not self.onePassword.is_authenticated():
            sys.exit(1)

