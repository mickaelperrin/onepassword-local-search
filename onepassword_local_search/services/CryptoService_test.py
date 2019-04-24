import pytest
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.tests.fixtures_common import common_data, op_session, crypto_service
from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.models.Item import Item



@pytest.mark.usefixtures("op_session")
def test_session_keys(crypto_service):
    crypto_service._get_base_keys()
    assert crypto_service.sessionKey == common_data('session_key')
    assert type(crypto_service.encryptedSessionPrivateKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSessionPrivateKey.iv == 'o86o5GT5zK7xh83e'
    assert crypto_service.encryptedSessionPrivateKey.data == 'Fn3jMEhlgsniiwP0wgSUF-HUR2LHEQuIW032Oz25VokclJG9t2Tl8a8KgDHgVwgypO2hQbS_0u2xteDEON4GVV7vf4C_7UmzbWIaz5qN1PXa5_AlnmBmHiRFXoTNEQgqJqxkEDHGnCaNExkw8FenArevjwKwp2Zwr1jIL0m8YVEnROSKg8WEuuOh74EehpkmypBJ-I4PIHe-C80OwqriwK6XK_3dEat6iYzvSYKQK4MwY5eTDSZWoIvaAFs8QHBez8CiaDmzIp1fgNOiYwplf9skc9ZA0cvUc9i0AT3aQa7PBsTHEQ2srgF43sS4eFF6X66QOmsbY4UAy-JjakOmIPkthkkx5dsGIsCUO1whAzIlmnTrNYUFtA'
    assert crypto_service.encryptedSessionPrivateKey.enc == 'A256GCM'
    assert crypto_service.sessionPrivateKey['encodedMuk'] == '2Zqlkn-ppcrz0RaH3wDUiKwu1YUPj1bRM09R9MEmsrE'
    assert crypto_service.sessionPrivateKey['encodedKey'] == 'JH84cS3eNebV8P0Kck3fviRSfnOk8WMFUtiF6umWHFY'

@pytest.mark.usefixtures("op_session")
def test_keyset(crypto_service):
    crypto_service._get_base_keys()
    assert crypto_service.symmetricKey['alg'] == 'A256GCM'
    assert crypto_service.symmetricKey['k'] == 'DTCXfnskB1Sm8QiMA_qCWxwZ4GmWOeyAreSN8c0pRcc'

@pytest.mark.usefixtures("op_session")
def test_private_key(crypto_service):
    crypto_service._get_base_keys()
    assert crypto_service.privateKey['alg'] == 'RSA-OAEP'
    assert crypto_service.privateKey['kid'] == 'vhhhcyj7rc3vocnd5o2iksiflm'
    assert crypto_service.privateKey['n'] == 'vOAZ3IwHI1bkkD5L_5uGvrtMV6KKjzK55ed02Tbqa5Z9k4tKNiwIMykNzmR3XSsNRRthQE6llIh8AJLCbypGnEuCKWZDYmkW_42dF26VjUQ5WqEdWniypsDBcSFqQzBbbb6yv_gs0FNG5QpsEBRuA5DeFSh86CSW-BY35GaARo1G9zDKoqyEI6vZGGX3gv9Nr0docD1Y8ducwkAPtFX4fhFTiBpvJeAGzlKk6imeknZiC4hDFOFt07_vJqORB4Y1crrixPE5E6xkutzgui3WdXBjL14RPIxgfT3_zwc_3Uyy71Y3Tr99MA-i2iWVpRDj9GS3lXh8m9ABp4O4AnU7YQ'

@pytest.mark.usefixtures("op_session")
def test_vault_key(crypto_service):
    vault_key = crypto_service._get_vault_key('6')
    assert vault_key['alg'] == 'A256GCM'
    assert vault_key['k'] == 'CF6mPDqu8Uklk2tfq4Vj5moILWpdxKZycIxQI1VUg1A'

@pytest.mark.usefixtures("op_session")
def test_vault_key(crypto_service):
    item = crypto_service.decrypt_item(Item(crypto_service.storageService.get_item_by_uuid(common_data('item_uuid'))))
    assert item.overview['title'] == 'Software licence'
    assert item.details['sections'][0]['fields'][1]['v'] == 'License number'
