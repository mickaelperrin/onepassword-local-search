import pytest
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.tests.fixtures_common import common_data, op_session, crypto_service
from onepassword_local_search.services.StorageService import StorageService



@pytest.mark.usefixtures("op_session")
def test_session_keys(crypto_service):
    assert crypto_service.sessionKey == common_data('session_key')
    assert type(crypto_service.encryptedSessionPrivateKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSessionPrivateKey.iv == 'o86o5GT5zK7xh83e'
    assert crypto_service.encryptedSessionPrivateKey.data == 'Fn3jMEhlgsniiwP0wgSUF-HUR2LHEQuIW032Oz25VokclJG9t2Tl8a8KgDHgVwgypO2hQbS_0u2xteDEON4GVV7vf4C_7UmzbWIaz5qN1PXa5_AlnmBmHiRFXoTNEQgqJqxkEDHGnCaNExkw8FenArevjwKwp2Zwr1jIL0m8YVEnROSKg8WEuuOh74EehpkmypBJ-I4PIHe-C80OwqriwK6XK_3dEat6iYzvSYKQK4MwY5eTDSZWoIvaAFs8QHBez8CiaDmzIp1fgNOiYwplf9skc9ZA0cvUc9i0AT3aQa7PBsTHEQ2srgF43sS4eFF6X66QOmsbY4UAy-JjakOmIPkthkkx5dsGIsCUO1whAzIlmnTrNYUFtA'
    assert crypto_service.encryptedSessionPrivateKey.enc == 'A256GCM'
    assert crypto_service.sessionPrivateKey['encodedMuk'] == '2Zqlkn-ppcrz0RaH3wDUiKwu1YUPj1bRM09R9MEmsrE'
    assert crypto_service.sessionPrivateKey['encodedKey'] == 'JH84cS3eNebV8P0Kck3fviRSfnOk8WMFUtiF6umWHFY'

@pytest.mark.usefixtures("op_session")
def test_keyset(crypto_service):
    assert crypto_service.symmetricKey['alg'] == 'A256GCM'
    assert crypto_service.symmetricKey['k'] == 'DTCXfnskB1Sm8QiMA_qCWxwZ4GmWOeyAreSN8c0pRcc'
