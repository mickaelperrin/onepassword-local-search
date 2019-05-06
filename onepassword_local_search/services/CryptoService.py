from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.models.Cipher import Cipher
from onepassword_local_search.lib.optestlib import aes_decrypt, get_binary_from_string, rsa_decrypt, determine_session_file_path_from_session_key
from os import environ as os_environ, path as os_path
from onepassword_local_search.exceptions.ManagedException import ManagedException
from json import loads as json_loads
from glob import glob as glob_glob


class CryptoService:

    accountId: int
    storageService: StorageService
    disable_session_caching: bool
    sessionKey: str
    encryptedSessionPrivateKey: Cipher
    encryptedSymmetricyKey: Cipher
    encryptedAccountKey: Cipher
    encryptedPrivateKey: Cipher
    configFileService: ConfigFileService
    accountKey: dict
    symmetricKey: dict
    privateKey: dict
    privateKeyRaw: str
    shorthand: str
    userUUID: str
    vaultKeys: dict = {}

    def __init__(self, storage_service: StorageService, config_file_service: ConfigFileService, account_id, disable_session_caching=False):
        self.storageService = storage_service
        self.configFileService = config_file_service
        self.userUUID = self.storageService.get_user_uuid_from_account_id(account_id)
        self.shorthand = self.configFileService.get_shorthand_from_user_uuid(self.userUUID)
        self.disable_session_caching = disable_session_caching
        if self.disable_session_caching:
            self.cleanup_sessions_cache()

    @staticmethod
    def cleanup_sessions_cache():
        for file in glob_glob(os_path.join(CryptoService._get_encrypted_session_directory_path(), '.*_cached')):
            import os
            os.remove(file)

    def _get_base_keys(self):
        self.sessionKey = self._get_session_key()
        self.encryptedSessionPrivateKey = self._get_encrypted_session_key()
        self.sessionPrivateKey = json_loads(self.decrypt(self.sessionKey, self.encryptedSessionPrivateKey))
        self.encryptedSymmetricyKey = Cipher(self._get_encrypted_symmetric_key())
        self.symmetricKey = json_loads(self.decrypt(self.sessionPrivateKey['encodedMuk'], self.encryptedSymmetricyKey))
        self.encryptedAccountKey = Cipher(self._get_encrypted_account_key())
        self.accountKey = json_loads(self.decrypt(self.symmetricKey['k'], self.encryptedAccountKey))
        self.encryptedPrivateKey = Cipher(self._get_encrypted_private_key())
        self.privateKeyRaw = self.decrypt(self.symmetricKey['k'], self.encryptedPrivateKey).decode('utf-8')
        self.privateKey = json_loads(self.privateKeyRaw)

    def _get_session_key(self):
        if not os_environ.get('OP_SESSION_' + self.shorthand):
            raise ManagedException('Environment variable OP_SESSION_team is not set for %s ' % self.shorthand)
        return os_environ.get('OP_SESSION_' + self.shorthand)

    @staticmethod
    def _get_encrypted_session_directory_path():
        if os_environ.get('OP_SESSION_PRIVATE_KEY_FOLDER'):
            path = os_environ.get('OP_SESSION_PRIVATE_KEY_FOLDER')
            if os_path.isdir(path):
                return path

        # TODO: implement for other platforms than MAC
        path = os_path.join(os_environ.get('TMPDIR'), 'com.agilebits.op.501')
        if not os_path.isdir(path):
            raise ManagedException('Session private folder is missing. Ensure you are signin with the onepassword cli (op).')
        return path

    def _get_encrypted_session_file_path(self):
        if os_environ.get('OP_SESSION_PRIVATE_KEY_FILE'):
            path = os_environ.get('OP_SESSION_PRIVATE_KEY_FILE')
            if os_path.isfile(path):
                return path
        filepath = os_path.join(self._get_encrypted_session_directory_path(), determine_session_file_path_from_session_key(self.sessionKey))
        if os_path.isfile(filepath):
            if not os_path.isfile(filepath + '_cached') and not self.disable_session_caching:
                from shutil import copyfile
                copyfile(filepath, filepath + '_cached')
        else:
            filepath += '_cached'
            if os_path.isfile(filepath):
                return filepath
            else:
                raise ManagedException('Unable to find session file')
        return filepath

    def _get_encrypted_session_key(self):
        with open(self._get_encrypted_session_file_path()) as f:
            return Cipher(f.read())

    def _get_encrypted_user_symmetric_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.userUUID)
        return self.storageService.get_encrypted_symmetric_key(account_id)

    def _get_encrypted_symmetric_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.userUUID)
        return self.storageService.get_encrypted_symmetric_key(account_id)

    def _get_encrypted_account_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.userUUID)
        return self.storageService.get_account_key(account_id)

    def _get_encrypted_private_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.userUUID)
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
        account_id = self.storageService.get_account_id_from_user_uuid(self.userUUID)
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

    def is_authenticated(self):
        try:
            self._get_base_keys()
            return True
        except:
            pass
            return False
