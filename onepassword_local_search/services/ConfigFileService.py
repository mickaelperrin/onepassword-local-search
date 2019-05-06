from os import environ as os_environ, path as os_path
from json import load as json_load
from onepassword_local_search.exceptions.ManagedException import ManagedException


class ConfigFileService:

    config: dict
    latest_signin: str

    def __init__(self):
        self.config = self._get_local_config()
        self.latest_signin = self.get_latest_signin()

    @staticmethod
    def _get_local_config():
        op_config_path = os_environ.get('ONEPASSWORD_CONFIG_FILE_PATH')
        if op_config_path:
            if not os_path.isfile(op_config_path):
                raise ManagedException('The env varialbe ONEPASSWORD_CONFIG_FILE_PATH speciies a missing file for OnePassword CLI configuration')
        else:
            op_config_path = os_path.join(os_environ.get('HOME'), '.op', 'config')
        if not os_path.isfile(op_config_path):
            raise ManagedException('OnePassword CLI configuration is not present. Ensure you have run op signin')
        with open(op_config_path) as op_config_file:
            return json_load(op_config_file)

    def get_latest_signin(self):
        if hasattr(self, 'latest_signin') and self.latest_signin:
            return self.latest_signin
        if not self.config.get('latest_signin'):
            raise ManagedException('Missing latest_signin information. Ensure you are sign in')
        return self.config.get('latest_signin')

    def get_user_uuid_from_latest_signin(self):
        for account in self.config['accounts']:
            if account['shorthand'] != self.get_latest_signin():
                continue
            else:
                return account['userUUID']

    def get_accounts(self):
        return self.config['accounts']

    def get_shorthand_from_user_uuid(self, user_uuid):
        for account in self.config['accounts']:
            if account['userUUID'] == user_uuid:
                return account['shorthand']
        raise ManagedException('Unable to find shorthand for account with user uuid %s' % user_uuid)

