from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.models.Cipher import Cipher
from onepassword_local_search.lib.optestlib import dec_aes_gcm, get_binary_from_string
from os import environ as os_environ, path as os_path
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from jwkest.jwk import RSAKey, load_jwks
import json
import glob


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
        self.sessionKey = self._get_session_key()
        self.encryptedSessionPrivateKey = self._get_encrypted_session_key()
        self.sessionPrivateKey = json.loads(self.decrypt(self.sessionKey, self.encryptedSessionPrivateKey))
        self.encyptedSymmetricyKey = Cipher(self._get_encrypted_symmetric_key())
        self.symmetricKey = json.loads(self.decrypt(self.sessionPrivateKey['encodedMuk'], self.encyptedSymmetricyKey))
        self.encryptedAccountKey = Cipher(self._get_encrypted_account_key())
        self.accountKey = json.loads(self.decrypt(self.symmetricKey['k'], self.encryptedAccountKey))
        self.encryptedPrivateKey = Cipher(self._get_encrypted_private_key())
        self.privateKeyRaw = self.decrypt(self.symmetricKey['k'], self.encryptedPrivateKey).decode('utf-8')
        self.privateKey = json.loads(self.privateKeyRaw)


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
        files = glob.glob(os_path.join(self._get_encrypted_session_directory_path(), '.*'))
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
        return dec_aes_gcm(
            ct=get_binary_from_string(cipher.data)[:-16],
            key=get_binary_from_string(key),
            iv=get_binary_from_string(cipher.iv),
            tag=get_binary_from_string(cipher.data)[-16:])

    def _rsa_decrypt(self, key_raw, ct):
        jwkj = '{"keys": [%s]}' % key_raw
        jwk = json.loads(jwkj)
        jwk = load_jwks(jwkj)[0]
        RSA_Key = RSA.construct((jwk.n, jwk.e, jwk.d))
        cipher = PKCS1_OAEP.new(RSA_Key)
        return cipher.decrypt(get_binary_from_string(ct))

    def _get_vault_key(self, vault_id):
        account_id = self.storageService.get_account_id_from_user_uuid(self.configFileService.get_user_uuid())
        encrypted_vault_key = json.loads(self.storageService.get_encrypted_vault_key(vault_id, account_id))
        return json.loads(self._rsa_decrypt(self.privateKeyRaw, encrypted_vault_key['data']).decode('utf-8'))

    def decrypt_item(self, item, part='full'):
        if not self.vaultKeys.get(item.vaultId):
            self.vaultKeys[item.vaultId] = self._get_vault_key(item.vaultId)

        if part == 'overview':
            item.overview = json.loads(self.decrypt(self.vaultKeys[item.vaultId]['k'], item.encryptedOverview).decode('utf-8'))
        elif part == 'details':
            item.details = json.loads(self.decrypt(self.vaultKeys[item.vaultId]['k'], item.encryptedDetails).decode('utf-8'))
        else:
            item.overview = json.loads(self.decrypt(self.vaultKeys[item.vaultId]['k'], item.encryptedOverview).decode('utf-8'))
            item.details = json.loads(self.decrypt(self.vaultKeys[item.vaultId]['k'], item.encryptedDetails).decode('utf-8'))

        return item



