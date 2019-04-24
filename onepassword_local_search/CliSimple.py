from .__version__ import __version__
from sys import exit
from onepassword_local_search.exceptions.ManagedException import ManagedException
from onepassword_local_search.OnePassword import OnePassword


class CliSimple:

    action: str
    field: str
    script_name: str
    uuid: str

    def __init__(self, script_name, action='version', uuid=None, field=None):
        self.field = field
        self.uuid = uuid
        self.action = action
        self.script_name = script_name

    def run(self):
        if self.action == 'get':
            if self.uuid is None:
                print('Error: UUID is required to get secret')
                print(self.usage())
                exit(1)
            return self.get(self.uuid, self.field)
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
    def version():
        print('Version: ' + __version__)
