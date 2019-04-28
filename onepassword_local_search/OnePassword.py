from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.models.Item import Item
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from re import sub as re_sub
import string


class OnePassword:

    storageService: StorageService
    cryptoService: CryptoService
    configFileService: ConfigFileService
    useCustomUUIDMapping: bool = False

    def __init__(self, use_custom_uuid=False):
        self.storageService = StorageService(use_custom_uuid)
        self.configFileService = ConfigFileService()
        self.cryptoService = CryptoService(self.storageService, self.configFileService)
        if use_custom_uuid:
            self._ensure_uuid_mapping_has_values()

    def _ensure_uuid_mapping_has_values(self):
        if not self.storageService.uuid_mapping_has_entries():
            self.mapping_update()

    def get(self, uuid, field=None, use_custom_mapping=False, output=True):
        encrypted_item = Item(self.storageService.get_item_by_uuid(uuid, use_custom_mapping))
        item = self.cryptoService.decrypt_item(encrypted_item)
        decrypted_field = item.get(field, output=output)
        if output:
            print(decrypted_field, end='')
        return decrypted_field

    def get_items(self, result_fitler):
        items = []
        for item in self.storageService.list():
            decrypted_item = self.cryptoService.decrypt_item(Item(item))
            if result_fitler is None or result_fitler in decrypted_item.overview['title']:
                items.append(decrypted_item)
        return items

    def list(self, result_format=None, result_fitler=None):
        class SimpleFormatter(string.Formatter):
            def get_value(self, key, args, kwargs):
                return item.get(key, strict=False)
        list_format = result_format if result_format else '{uuid} {title}'
        sf = SimpleFormatter()
        for item in self.get_items(result_fitler):
            print(sf.format(list_format, item).strip())

    def mapping(self, subcommand):
        self.storageService.checks_for_uuid_mapping()
        return getattr(self, 'mapping_' + subcommand)()

    def mapping_update(self):
        self.storageService.truncate_uuid_mapping_table()
        for item in self.storageService.list():
            decrypted_item = self.cryptoService.decrypt_item(Item(item))
            custom_uuid = decrypted_item.get('UUID', strict=False)
            if custom_uuid:
                self.storageService.add_uuid_mapping(custom_uuid, decrypted_item.uuid)
        self.storageService.con.commit()

    def mapping_list(self):
        for item in self.storageService.list_mapping():
            print("%s <-> %s" % (item['op_uuid'], item['custom_uuid']))

    @staticmethod
    def version():
        from .__version__ import __version__
        print('Version: ' + __version__)

    def is_authenticated(self):
        return self.cryptoService.is_authenticated()
