import pytest
from os import environ, path
from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from os import path as os_path
from pytest_mock import mocker
from json import loads as json_loads


def common_data(item):
    return dict(
        nl='\n',
        item_uuid='e25haqmocd5ifiymorfzwxnzry',
        login_uuid='zzfmhu2j7ajq55mmpm3ihs3oqy',
        subdomain='onepassword_local_search',
        session_key='azuDId6PvlUtwsLQZD-4jzGpMxUxRNQOxEgcdbZhppI'
    ).get(item)


@pytest.fixture
def no_op_session(monkeypatch, mocker):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), 'B5.sqlite'))
    if environ.get('OP_SESSION_' + common_data('subdomain')):
        monkeypatch.delenv('OP_SESSION_' + common_data('subdomain'))
    mocker.patch.object(ConfigFileService, '_get_local_config')
    with open(os_path.join(os_path.dirname(__file__), 'config'), 'r') as f:
        config = f.read()
        f.close()
    ConfigFileService._get_local_config.return_value = json_loads(config)


@pytest.fixture
def op_session(monkeypatch, mocker):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), 'B5.sqlite'))
    monkeypatch.setenv('OP_SESSION_' + common_data('subdomain'), common_data('session_key'))
    monkeypatch.setenv('OP_SESSION_PRIVATE_KEY_FILE', path.join(path.dirname(__file__), '.Y_efcm4Gd_W4NnRTMeOuSEHPA5w'))
    mocker.patch.object(ConfigFileService, '_get_local_config')
    with open(os_path.join(os_path.dirname(__file__), 'config'), 'r') as f:
        config = f.read()
        f.close()
    ConfigFileService._get_local_config.return_value = json_loads(config)


@pytest.fixture
def storage_service(monkeypatch):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), 'B5.sqlite'))
    return StorageService()

@pytest.mark.usefixtures("op_session")
@pytest.fixture
def crypto_service(mocker):
    mocker.patch.object(CryptoService, '_get_encrypted_session_file_path')
    CryptoService._get_encrypted_session_file_path.return_value = os_path.join(os_path.dirname(os_path.dirname(__file__, )), 'tests', '.Y_efcm4Gd_W4NnRTMeOuSEHPA5w')
    return CryptoService(StorageService(), ConfigFileService())