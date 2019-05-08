from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.models.Item import Item
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.services.AccountService import AccountService
from onepassword_local_search.exceptions.ManagedException import ManagedException
from onepassword_local_search.lib.utils import SimpleFormatter


class OnePassword:

    storageService: StorageService
    cryptoService: CryptoService
    configFileService: ConfigFileService
    accountService: AccountService

    def __init__(self, custom_uuid_mapping=None, disable_session_caching=False):
        self.storageService = StorageService(custom_uuid_mapping)
        self.configFileService = ConfigFileService()
        self.accountService = AccountService(self.storageService, self.configFileService, disable_session_caching=disable_session_caching)
        if custom_uuid_mapping:
            self._ensure_uuid_mapping_has_values()

    def _ensure_uuid_mapping_has_values(self):
        if not self.storageService.uuid_mapping_has_entries():
            self.mapping_update()

    def can_decrypt(self, item):
        return item.vaultId in self.accountService.available_vaults_id

    def get(self, uuid, field=None, custom_mapping=None, output=True):
        encrypted_item = Item(self.storageService.get_item_by_uuid(uuid, custom_mapping))
        if not self.can_decrypt(encrypted_item):
            raise ManagedException('You are not connected to the required account to decrypt item: %s' % uuid)
        decryptor = self.accountService.get_decryptor(encrypted_item.vaultId)
        item = decryptor.decrypt_item(encrypted_item)
        decrypted_field = item.get(field, output=output)
        if output:
            print(decrypted_field, end='')
        return decrypted_field

    def get_items(self, result_fitler):
        items = []
        for item in self.storageService.list(self.accountService.get_available_accounts_id()):
            encrypted_item = Item(item)
            decryptor = self.accountService.get_decryptor(encrypted_item.vaultId)
            decrypted_item = decryptor.decrypt_item(encrypted_item)
            if result_fitler is None or result_fitler in decrypted_item.overview['title']:
                items.append(decrypted_item)
        return items

    def list(self, result_format=None, result_fitler=None, result_encoding=None):
        list_format = result_format if result_format else '{uuid} {title}'
        sf = SimpleFormatter(output_encoding=result_encoding)
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
        for item in self.storageService.list(self.accountService.get_available_accounts_id()):
            encrypted_item = Item(item)
            decryptor = self.accountService.get_decryptor(encrypted_item.vaultId)
            decrypted_item = decryptor.decrypt_item(encrypted_item)
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

    def is_authenticated(self, user_uuids=None):
        try:
            if self.accountService.cryptoServices == {}:
                self.accountService.cryptoServices = self.accountService.set_crypto_services()
        except Exception:
            pass
        if user_uuids is None:
            user_uuids = [self.configFileService.get_user_uuid_from_latest_signin()]
        if isinstance(user_uuids, str):
            user_uuids = [user_uuids]
        for user_uuid in user_uuids:
            account_id = self.storageService.get_account_id_from_user_uuid(user_uuid)
            if account_id in self.accountService.cryptoServices.keys():
                try:
                    if not self.accountService.cryptoServices[account_id].is_authenticated():
                        return False
                except:
                    return False
            else:
                return False
        return True
