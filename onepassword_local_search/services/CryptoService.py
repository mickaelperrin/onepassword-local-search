from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.models.Cipher import Cipher
from onepassword_local_search.lib.optestlib import aes_decrypt, get_binary_from_string, rsa_decrypt
from os import environ as os_environ, path as os_path
from json import loads as json_loads
from glob import glob as glob_glob


class CryptoService:

    storageService: StorageService
    sessionKey: str
    encryptedSessionPrivateKey: Cipher
    encyptedSymmetricyKey: Cipher
    encryptedAccountKey: Cipher
    ecnryptedPrivateKey: Cipher
    configFileService: ConfigFileService
    accountKey: dict
    symmetricKey: dict
    privateKey: dict
    privateKeyRaw: str
    vaultKeys: dict = {}

    def __init__(self, storage_service: StorageService, config_file_service: ConfigFileService):
        self.storageService = storage_service
        self.configFileService = config_file_service

    def _get_base_keys(self):
        self.sessionKey = self._get_session_key()
        self.encryptedSessionPrivateKey = self._get_encrypted_session_key()
        self.sessionPrivateKey = json_loads(self.decrypt(self.sessionKey, self.encryptedSessionPrivateKey))
        self.encyptedSymmetricyKey = Cipher(self._get_encrypted_symmetric_key())
        self.symmetricKey = json_loads(self.decrypt(self.sessionPrivateKey['encodedMuk'], self.encyptedSymmetricyKey))
        self.encryptedAccountKey = Cipher(self._get_encrypted_account_key())
        self.accountKey = json_loads(self.decrypt(self.symmetricKey['k'], self.encryptedAccountKey))
        self.encryptedPrivateKey = Cipher(self._get_encrypted_private_key())
        self.privateKeyRaw = self.decrypt(self.symmetricKey['k'], self.encryptedPrivateKey).decode('utf-8')
        self.privateKey = json_loads(self.privateKeyRaw)

    def _get_session_key(self):
        latest_signin = self.configFileService.get_latest_signin()
        if not os_environ.get('OP_SESSION_' + latest_signin):
            print('Environment variable OP_SESSION_team is not set.')
            exit(1)
        return os_environ.get('OP_SESSION_' + latest_signin)

    def _get_encrypted_session_directory_path(self):
        if os_environ.get('OP_SESSION_PRIVATE_KEY_FOLDER'):
            path = os_environ.get('OP_SESSION_PRIVATE_KEY_FOLDER')
            if os_path.isdir(path):
                return path

        # TODO: implement for other platforms than MAC
        path = os_path.join(os_environ.get('TMPDIR'), 'com.agilebits.op.501')
        if not os_path.isdir(path):
            raise Exception('Session private folder is missing. Ensure you are signin with the onepassword cli (op).')
        return path

    def _get_encrypted_session_file_path(self):
        if os_environ.get('OP_SESSION_PRIVATE_KEY_FILE'):
            path = os_environ.get('OP_SESSION_PRIVATE_KEY_FILE')
            if os_path.isfile(path):
                return path
        files = glob_glob(os_path.join(self._get_encrypted_session_directory_path(), '.*'))
        return max(files, key=os_path.getctime)

    def _get_encrypted_session_key(self):
        with open(self._get_encrypted_session_file_path()) as f:
            return Cipher(f.read())

    def _get_encrypted_symmetric_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.configFileService.get_user_uuid())
        return self.storageService.get_encrypted_symmetric_key(account_id)

    def _get_encrypted_account_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.configFileService.get_user_uuid())
        return self.storageService.get_account_key(account_id)

    def _get_encrypted_private_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.configFileService.get_user_uuid())
        return self.storageService.get_encrypted_private_key(account_id)

    def decrypt(self, key, cipher: Cipher):
        return aes_decrypt(
            ct=get_binary_from_string(cipher.data)[:-16],
            key=get_binary_from_string(key),
            iv=get_binary_from_string(cipher.iv),
            tag=get_binary_from_string(cipher.data)[-16:])

    def _get_vault_key(self, vault_id):
        if not hasattr(self, 'privateKeyRaw') or not self.privateKeyRaw:
            self._get_base_keys()
        account_id = self.storageService.get_account_id_from_user_uuid(self.configFileService.get_user_uuid())
        encrypted_vault_key = json_loads(self.storageService.get_encrypted_vault_key(vault_id, account_id))
        return json_loads(rsa_decrypt(self.privateKeyRaw, encrypted_vault_key['data']).decode('utf-8'))

    def decrypt_item(self, item, part='full'):
        vault_key = None
        if os_environ.get('VAULT_%s_KEY' % item.vaultId):
            vault_key = os_environ.get('VAULT_%s_KEY' % item.vaultId)
        elif not self.vaultKeys.get(item.vaultId):
            self.vaultKeys[item.vaultId] = self._get_vault_key(item.vaultId)
        if not vault_key:
            vault_key = self.vaultKeys[item.vaultId]['k']

        if part == 'overview':
            item.overview = json_loads(self.decrypt(vault_key, item.encryptedOverview).decode('utf-8'))
        elif part == 'details':
            item.details = json_loads(self.decrypt(vault_key, item.encryptedDetails).decode('utf-8'))
        else:
            item.overview = json_loads(self.decrypt(vault_key, item.encryptedOverview).decode('utf-8'))
            item.details = json_loads(self.decrypt(vault_key, item.encryptedDetails).decode('utf-8'))

        return item



