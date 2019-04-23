import pytest
from onepassword_local_search.CliSimple import CliSimple
from onepassword_local_search.__version__ import __version__
from onepassword_local_search.tests.fixtures_common import common_data, no_op_session

nl = common_data("nl")


@pytest.fixture
def cli_version():
    return CliSimple('script', 'version')


def test_version(cli_version, capsys):
    cli_version.run()
    std = capsys.readouterr()
    assert std.out == 'Version: ' + __version__ + nl


@pytest.fixture
def cli_get_uuid():
    return CliSimple('script', 'get', common_data('uuid_test'), 'password')


@pytest.mark.usefixtures("no_op_session")
def test_get_uuid(cli_get_uuid, capsys):
    with pytest.raises(SystemExit) as exit_code:
        cli_get_uuid.run()
    std = capsys.readouterr()
    assert std.out.find('OP_SESSION_team is not set') != -1
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1