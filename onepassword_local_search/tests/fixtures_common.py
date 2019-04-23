import pytest
from os import environ, path


def common_data(item):
    return dict(
        nl='\n',
        uuid_test='i7jf563zcbgp7je56hfqriwhsu'
    ).get(item)


@pytest.fixture
def no_op_session(monkeypatch):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), 'B5.sqlite'))
    if environ.get('OP_SESSION_onepassword_local_search'):
        monkeypatch.delenv('OP_SESSION_onepassword_local_search')