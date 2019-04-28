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
    useCustomUUIDMapping: bool = False

    def __init__(self, args):
        self.args = args
        if 'use_custom_uuid' in self.args.__dict__.keys():
            self.useCustomUUIDMapping = self.args.use_custom_uuid
        self.storageService = StorageService(self.useCustomUUIDMapping)
        self.configFileService = ConfigFileService()
        self.cryptoService = CryptoService(self.storageService, self.configFileService)
        if self.useCustomUUIDMapping:
            self._ensure_uuid_mapping_has_values()

    def _ensure_uuid_mapping_has_values(self):
        if not self.storageService.uuid_mapping_has_entries():
            self.mapping_update()

    def get(self):
        encrypted_item = Item(self.storageService.get_item_by_uuid(self.args.uuid, self.useCustomUUIDMapping))
        item = self.cryptoService.decrypt_item(encrypted_item)
        decrypted_field = item.get(self.args.field)
        print(decrypted_field, end='')
        return decrypted_field

    def get_items(self, filter):
        items = []
        for item in self.storageService.list():
            decrypted_item = self.cryptoService.decrypt_item(Item(item))
            if filter is None or filter in decrypted_item.overview['title']:
                items.append(decrypted_item)
        return items

    def list(self):
        class SimpleFormatter(string.Formatter):
            def get_value(self, key, args, kwargs):
                return item.get(key, strict=False)
        list_format = self.args.format if self.args.format else '{uuid} {title}'
        sf = SimpleFormatter()
        for item in self.get_items(self.args.filter):
            print(sf.format(list_format, item).strip())

    def mapping(self):
        self.storageService.checks_for_uuid_mapping()
        return getattr(self, 'mapping_' + self.args.subcommand)()

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
