import pytest
from onepassword_local_search.CliSimple import CliSimple
from onepassword_local_search.__version__ import __version__
from onepassword_local_search.tests.fixtures_common import common_data

nl = common_data("nl")


@pytest.fixture
def cli_version():
    return CliSimple('script', 'version')


def test_version(cli_version, capsys):
    cli_version.run()
    std = capsys.readouterr()
    assert std.out == 'Version: ' + __version__ + nl