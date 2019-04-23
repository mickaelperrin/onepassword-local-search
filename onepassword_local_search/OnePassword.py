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

    def _get_encrypted_item(self, uuid):
        return Item(self.storageService.get_item_by_uuid(uuid))

    def get(self, uuid, field):
        encrypted_item = self._get_encrypted_item(uuid)
        print('get')
