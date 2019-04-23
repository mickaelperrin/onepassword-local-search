import pytest
from onepassword_local_search.tests.fixtures_common import storage_service, common_data


def test_item_query(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('item_uuid'))
    assert enc_item['uuid'] == common_data('item_uuid')
