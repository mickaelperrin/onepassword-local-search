import json
from os import environ, path
from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.models.Item import Item


class OnePassword:

    storageService: StorageService
    cryptoService: CryptoService

    def __init__(self):
        self.storageService = StorageService()
        self.cryptoService = CryptoService(self.storageService)

    @staticmethod
    def _exit_if_no_session():
        op_config_path = path.join(environ.get('HOME'), '.op', 'config')
        if not path.isfile(op_config_path):
            print('OnePassword CLI configuration is not present. Ensure you have run op signin')
            exit(1)
        with open(op_config_path) as op_config_file:
            config = json.load(op_config_file)
        if not config.get('latest_signin'):
            print('Missing latest_signin information. Ensure you are sign in')
            exit(1)
        if not environ.get('OP_SESSION_' + config.get('latest_signin')):
            print('Environment variable OP_SESSION_team is not set.')
            exit(1)

    def _get_encrypted_item(self, uuid):
        return Item(self.storageService.get_item_by_uuid(uuid))

    def get(self, uuid, field):
        self._exit_if_no_session()
        encrypted_item = self._get_encrypted_item(uuid)
        print('get')
