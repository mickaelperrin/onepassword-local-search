import pytest
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.tests.fixtures_common import common_data, op_session
from onepassword_local_search.services.StorageService import StorageService

@pytest.mark.usefixtures("op_session")
@pytest.fixture
def crypto_service(monkeypatch):
    return CryptoService(StorageService())


@pytest.mark.usefixtures("op_session")
def test_session_keys(crypto_service):
    assert crypto_service.sessionKey == common_data('session_key')
    assert type(crypto_service.encryptedSessionPrivateKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSessionPrivateKey.iv == 'oUUfx3o33w5wDS8K'
    assert crypto_service.encryptedSessionPrivateKey.data == 'umdgCCC48wRSBaRMOCoAkgcE6nOerQo52IIF8bO9okCyzCmF5P4pKo-NA-1_V5xN1fEXxKe-J1PQGVaxlFo6B3ezGwQlB7pWjXd6gmZmBBo8H15rqIvwz843TE7pw8DJ_mGBZuGXfH5_O7L36CbiEAhiQnTQezZ2KJ_8KMjdad_H6SHWDCyY93iH8nWA62UPusXL5B1T21lW0k47dvYw1lEgJLWvdXtysY2gMtbCFMuvM6jrGliRVCQRml3q5Jff9-4qsOHt4HMr9Ik2RhK-Uz3vsqreI6HJxRQ9JcbHfUdr7wzFqDT9eiMNUsFz9vp9hCU_LL-SXkZyls05nzZVSxvqOyN-wegx9xenxB1R170wHKjcCM2BVA'

