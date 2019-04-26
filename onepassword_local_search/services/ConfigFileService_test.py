import pytest
import os
import json
from pytest_mock import mocker
from onepassword_local_search.services.ConfigFileService import ConfigFileService


def test_without_env_var(mocker):
    mocker.patch.object(ConfigFileService, '_get_local_config')
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'config'), 'r') as f:
        config = f.read()
        f.close()
    ConfigFileService._get_local_config.return_value = json.loads(config)
    config_file_service = ConfigFileService()
    assert config_file_service.latest_signin == 'onepassword_local_search'


def test_with_env_var(monkeypatch):
    monkeypatch.setenv('ONEPASSWORD_CONFIG_FILE_PATH', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'config'))
    config_file_service = ConfigFileService()
    assert config_file_service.latest_signin == 'onepassword_local_search'