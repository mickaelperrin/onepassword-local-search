from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.models.Item import Item
from onepassword_local_search.services.ConfigFileService import ConfigFileService
import string


class OnePassword:

    storageService: StorageService
    cryptoService: CryptoService
    configFileService: ConfigFileService

    def __init__(self, custom_uuid_mapping=None):
        self.storageService = StorageService(custom_uuid_mapping)
        self.configFileService = ConfigFileService()
        self.cryptoService = CryptoService(self.storageService, self.configFileService)
        if custom_uuid_mapping:
            self._ensure_uuid_mapping_has_values()

    def _ensure_uuid_mapping_has_values(self):
        if not self.storageService.uuid_mapping_has_entries():
            self.mapping_update()

    def get(self, uuid, field=None, custom_mapping=None, output=True):
        encrypted_item = Item(self.storageService.get_item_by_uuid(uuid, custom_mapping))
        item = self.cryptoService.decrypt_item(encrypted_item)
        decrypted_field = item.get(field, output=output)
        if output:
            print(decrypted_field, end='')
        return decrypted_field

    def get_items(self, result_fitler):
        items = []
        for item in self.storageService.list(self.configFileService.get_user_uuid()):
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

    def mapping(self, subcommand, use_lastpass_uuid=False):
        self.storageService.checks_for_uuid_mapping()
        if subcommand == 'list':
            self.mapping_list(use_lastpass_uuid)
        else:
            return getattr(self, 'mapping_' + subcommand)()

    def mapping_update(self):
        self.storageService.truncate_uuid_mapping_table()
        for item in self.storageService.list(self.configFileService.get_user_uuid()):
            decrypted_item = self.cryptoService.decrypt_item(Item(item))
            custom_uuid = decrypted_item.get('UUID', strict=False)
            lastpass_uuid = decrypted_item.get('LASTPASS_ID', strict=False)
            if custom_uuid:
                self.storageService.add_uuid_mapping(custom_uuid=custom_uuid, op_uuid=decrypted_item.uuid,
                                                     lpass_uuid=lastpass_uuid)
        self.storageService.con.commit()

    def mapping_list(self, use_lastpass_uuid=False):
        mapping_field_to_use = 'lpass_uuid' if use_lastpass_uuid else 'custom_uuid'
        for item in self.storageService.list_mapping():
            print("%s <-> %s" % (item['op_uuid'], item[mapping_field_to_use]))

    @staticmethod
    def version():
        from .__version__ import __version__
        print('Version: ' + __version__)

    def is_authenticated(self):
        return self.cryptoService.is_authenticated()
