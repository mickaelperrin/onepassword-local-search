from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.models.Cipher import Cipher
from onepassword_local_search.lib.optestlib import dec_aes_gcm, get_binary_from_string
from os import environ as os_environ, path as os_path
import json
import glob


class CryptoService:

    storageService: StorageService
    sessionKey: str
    encryptedSessionPrivateKey: Cipher
    encyptedSymmetricyKey: Cipher
    configFileService: ConfigFileService

    def __init__(self, storage_service: StorageService, config_file_service: ConfigFileService):
        self.storageService = storage_service
        self.configFileService = config_file_service
        self.sessionKey = self._get_session_key()
        self.encryptedSessionPrivateKey = self._get_encrypted_session_key()
        self.sessionPrivateKey = json.loads(self.decrypt('sessionPrivateKey', self.encryptedSessionPrivateKey))
        self.encyptedSymmetricyKey = Cipher(self._get_encrypted_symmetric_key())
        self.symmetricKey = json.loads(self.decrypt('symmetricKey', self.encyptedSymmetricyKey))

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
        files = glob.glob(os_path.join(self._get_encrypted_session_directory_path(), '.*'))
        return max(files, key=os_path.getctime)

    def _get_encrypted_session_key(self):
        with open(self._get_encrypted_session_file_path()) as f:
            return Cipher(f.read())

    def _get_encrypted_symmetric_key(self):
        account_id = self.storageService.get_account_id_from_user_uuid(self.configFileService.get_user_uuid())
        return self.storageService.get_encrypted_symmetric_key(account_id)

    def decrypt(self, key_type, cipher: Cipher):
        if key_type == 'sessionPrivateKey':
            return dec_aes_gcm(
                ct=get_binary_from_string(cipher.data)[:-16],
                key=get_binary_from_string(self.sessionKey),
                iv=get_binary_from_string(cipher.iv),
                tag=get_binary_from_string(cipher.data)[-16:])
        elif key_type == 'symmetricKey':
            return dec_aes_gcm(
                ct=get_binary_from_string(cipher.data)[:-16],
                key=get_binary_from_string(self.sessionPrivateKey['encodedMuk']),
                iv=get_binary_from_string(cipher.iv),
                tag=get_binary_from_string(cipher.data)[-16:])
