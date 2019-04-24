import pytest
from onepassword_local_search.OnePassword import OnePassword
from onepassword_local_search.tests.fixtures_common import common_data, op_session, crypto_service


@pytest.mark.usefixtures("op_session")
def test_get_encrypted_item(crypto_service):
    OnePassword.cryptoService = crypto_service
    item = OnePassword()._get_encrypted_item(common_data('item_uuid'))
    assert item.uuid == common_data('item_uuid')



