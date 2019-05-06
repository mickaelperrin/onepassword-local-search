import pytest
from onepassword_local_search.tests.fixtures_common import storage_service, common_data


def test_item_query(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('item_uuid'))
    assert enc_item['uuid'] == common_data('item_uuid')


def test_item_query_auto_1password(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('login_uuid'))
    assert enc_item['uuid'] == common_data('login_uuid')


def test_item_query_auto_lastpass(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('login_lastpass_uuid'))
    assert enc_item['uuid'] == common_data('login_uuid')


def test_item_query_auto_custom(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('login_custom_uuid'))
    assert enc_item['uuid'] == common_data('login_uuid')