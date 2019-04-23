from onepassword_local_search.services.StorageService import StorageService
from os import environ as os_environ, path as os_path
import json


class CryptoService:

    storageService: StorageService
    localConfig: dict
    sessionKey: str

    def __init__(self, storage_service: StorageService):
        self.storageService = storage_service
        self.localConfig = self._get_local_config()
        self.sessionKey = self._get_session_key()

    def _get_local_config(self):
        op_config_path = os_path.join(os_environ.get('HOME'), '.op', 'config')
        if not os_path.isfile(op_config_path):
            print('OnePassword CLI configuration is not present. Ensure you have run op signin')
            exit(1)
        with open(op_config_path) as op_config_file:
            return json.load(op_config_file)

    def _get_session_key(self):
        if not self.localConfig.get('latest_signin'):
            print('Missing latest_signin information. Ensure you are sign in')
            exit(1)
        if not os_environ.get('OP_SESSION_' + self.localConfig.get('latest_signin')):
            print('Environment variable OP_SESSION_team is not set.')
            exit(1)
        return os_environ.get('OP_SESSION_' + self.localConfig.get('latest_signin'))

