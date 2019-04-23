from onepassword_local_search.services.StorageService import StorageService


class CryptoService:

    def __init__(self, storage_service: StorageService):
        self.storageService = storage_service


