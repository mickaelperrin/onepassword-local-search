from os import environ as os_environ, path as os_path
import json


class ConfigFileService:

    config: dict
    latest_signin: str

    def __init__(self):
        self.config = self._get_local_config()
        self.latest_signin = self.get_latest_signin()

    @staticmethod
    def _get_local_config():
        op_config_path = os_path.join(os_environ.get('HOME'), '.op', 'config')
        if not os_path.isfile(op_config_path):
            print('OnePassword CLI configuration is not present. Ensure you have run op signin')
            exit(1)
        with open(op_config_path) as op_config_file:
            return json.load(op_config_file)

    def get_latest_signin(self):
        if hasattr(self, 'latest_signin') and self.latest_signin:
            return self.latest_signin
        if not self.config.get('latest_signin'):
            print('Missing latest_signin information. Ensure you are sign in')
            exit(1)
        return self.config.get('latest_signin')

    def get_user_uuid(self):
        for account in self.config['accounts']:
            if account['shorthand'] != self.get_latest_signin():
                continue
            else:
                return account['userUUID']