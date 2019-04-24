import pytest
from os import environ, path
from onepassword_local_search.services.StorageService import StorageService


def common_data(item):
    return dict(
        nl='\n',
        item_uuid='i7jf563zcbgp7je56hfqriwhsu',
        subdomain='onepassword_local_search',
        session_key='yA25KnTXfIvmPnOoLJ9tst9O37h8Kl2cPowam2d2d1U'
    ).get(item)


@pytest.fixture
def no_op_session(monkeypatch):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), 'B5.sqlite'))
    if environ.get('OP_SESSION_' + common_data('subdomain')):
        monkeypatch.delenv('OP_SESSION_' + common_data('subdomain'))


@pytest.fixture
def op_session(monkeypatch):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), 'B5.sqlite'))
    monkeypatch.setenv('OP_SESSION_' + common_data('subdomain'), common_data('session_key'))
    monkeypatch.setenv('OP_SESSION_PRIVATE_KEY_FOLDER', path.dirname(__file__))


@pytest.fixture
def storage_service(monkeypatch):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), 'B5.sqlite'))
    return StorageService()
