from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.models.Item import Item
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from re import sub as re_sub
import string
from argparse import Namespace


class OnePassword:

    args: Namespace
    storageService: StorageService
    cryptoService: CryptoService
    configFileService: ConfigFileService

    def __init__(self):
        self.storageService = StorageService()
        self.args = args
        self.configFileService = ConfigFileService()
        self.cryptoService = CryptoService(self.storageService, self.configFileService)

    def _get_encrypted_item(self, uuid):
        return Item(self.storageService.get_item_by_uuid(uuid))

    def get(self, args):
        encrypted_item = self._get_encrypted_item(args.uuid)
        item = self.cryptoService.decrypt_item(encrypted_item)
        decrypted_field = item.get(args.field)
        print(decrypted_field, end='')
        return decrypted_field

    def list(self):
        class SimpleFormatter(string.Formatter):
            def get_value(self, key, args, kwargs):
                return decrypted_item.get(key, strict=False)
        list_format = self.args.format if self.args.format else '{uuid} {title}'
        sf = SimpleFormatter()
        for item in self.storageService.list():
            decrypted_item = self.cryptoService.decrypt_item(Item(item))
            print(sf.format(list_format, decrypted_item).strip())

