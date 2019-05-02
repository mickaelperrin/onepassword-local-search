from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from os import environ as os_environ


class AccountService:

    accounts: []
    existing_accounts: []
    storageService: StorageService
    configFileService: ConfigFileService

    def __init__(self, storage_service: StorageService, config_file_service: ConfigFileService):
        self.storageService = storage_service
        self.configFileService = config_file_service
        self.existing_accounts = self.configFileService.get_accounts()
        self.accounts = self.get_available_accounts()

    def get_available_accounts(self):
        accounts = []
        for account in self.existing_accounts:
            if not os_environ.get('OP_SESSION_' + account['shorthand']):
                continue
            account_id = self.storageService.get_account_id_from_user_uuid(account['userUUID'])
            if account_id:
                account['id'] = account_id
                accounts.append(account)
        return accounts




