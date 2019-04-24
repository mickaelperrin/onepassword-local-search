from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.models.Item import Item
from onepassword_local_search.services.ConfigFileService import ConfigFileService


class OnePassword:

    storageService: StorageService
    cryptoService: CryptoService
    configFileService: ConfigFileService

    def __init__(self):
        self.storageService = StorageService()
        self.configFileService = ConfigFileService()
        self.cryptoService = CryptoService(self.storageService, self.configFileService)

    def _get_encrypted_item(self, uuid):
        return Item(self.storageService.get_item_by_uuid(uuid))

    def get(self, uuid, field=None):
        encrypted_item = self._get_encrypted_item(uuid)
        item = self.cryptoService.decrypt_item(encrypted_item)
        decrypted_field = item.get(field)
        print(decrypted_field, end='')
        return decrypted_field
