from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.models.Cipher import Cipher
from onepassword_local_search.lib.optestlib import dec_aes_gcm, get_binary_from_string
from os import environ as os_environ, path as os_path
import json
import glob


class CryptoService:

    storageService: StorageService
    localConfig: dict
    sessionKey: str
    encryptedSessionPrivateKey: Cipher

    def __init__(self, storage_service: StorageService):
        self.storageService = storage_service
        self.localConfig = self._get_local_config()
        self.sessionKey = self._get_session_key()
        self.encryptedSessionPrivateKey = self._get_encrypted_session_key()
        self.sessionPrivateKey = json.loads(self.decrypt('sessionPrivateKey', self.encryptedSessionPrivateKey))

    def _get_local_config(self):
        op_config_path = os_path.join(os_environ.get('HOME'), '.op', 'config')
        if not os_path.isfile(op_config_path):
            print('OnePassword CLI configuration is not present. Ensure you have run op signin')
            exit(1)
        with open(op_config_path) as op_config_file:
            return json.load(op_config_file)

    def _get_session_key(self):
        if not self.localConfig.get('latest_signin'):
            print('Missing latest_signin information. Ensure you are sign in')
            exit(1)
        if not os_environ.get('OP_SESSION_' + self.localConfig.get('latest_signin')):
            print('Environment variable OP_SESSION_team is not set.')
            exit(1)
        return os_environ.get('OP_SESSION_' + self.localConfig.get('latest_signin'))

    def _get_encrypted_session_directory_path(self):
        if os_environ.get('OP_SESSION_PRIVATE_KEY_FOLDER'):
            path = os_environ.get('OP_SESSION_PRIVATE_KEY_FOLDER')
            if os_path.isdir(path):
                return path

        # TODO: implement for other platforms than MAC
        path = os_path.join(os_environ.get('TMPDIR'), 'com.agilebits.op.501')
        if not os_path.isdir(path):
            raise Exception('Session private folder is missing')
        return path

    def _get_encrypted_session_file_path(self):
        files = glob.glob(os_path.join(self._get_encrypted_session_directory_path(), '.*'))
        return max(files, key=os_path.getctime)

    def _get_encrypted_session_key(self):
        with open(self._get_encrypted_session_file_path()) as f:
            return Cipher(f.read())

    def decrypt(self, type, cipher: Cipher):
        if type == 'sessionPrivateKey':
            return dec_aes_gcm(
                ct=get_binary_from_string(cipher.data)[:-16],
                key=get_binary_from_string(self.sessionKey),
                iv=get_binary_from_string(cipher.iv),
                tag=get_binary_from_string(cipher.data)[-16:])
