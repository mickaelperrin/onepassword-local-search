import pytest
from onepassword_local_search.CliSimple import CliSimple
from onepassword_local_search.__version__ import __version__
from onepassword_local_search.tests.fixtures_common import common_data, no_op_session, op_session

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
    return CliSimple('script', 'get', common_data('item_uuid'), 'password')


@pytest.mark.usefixtures("no_op_session")
def test_get_uuid(cli_get_uuid, capsys):
    with pytest.raises(SystemExit) as exit_code:
        cli_get_uuid.run()
    std = capsys.readouterr()
    assert std.out.find('OP_SESSION_team is not set') != -1
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1


@pytest.mark.usefixtures("op_session")
def test_get_title(capsys):
    CliSimple('script', 'get', common_data('item_uuid'), 'title').run()
    std = capsys.readouterr()
    assert std.out == 'Software licence'


@pytest.mark.usefixtures("op_session")
def test_get_login_title(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'title').run()
    std = capsys.readouterr()
    assert std.out == 'Connexion'


@pytest.mark.usefixtures("op_session")
def test_get_login_uuid(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'uuid').run()
    std = capsys.readouterr()
    assert std.out == 'zzfmhu2j7ajq55mmpm3ihs3oqy'


@pytest.mark.usefixtures("op_session")
def test_get_login_url(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'url').run()
    std = capsys.readouterr()
    assert std.out == 'https://site1.com'


@pytest.mark.usefixtures("op_session")
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'username').run()
    std = capsys.readouterr()
    assert std.out == 'username'


@pytest.mark.usefixtures("op_session")
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'password').run()
    std = capsys.readouterr()
    assert std.out == 'password'


@pytest.mark.usefixtures("op_session")
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'Section1;;Section1Field1').run()
    std = capsys.readouterr()
    assert std.out == 'Section1Field1Value'


@pytest.mark.usefixtures("op_session")
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'Section2;;Section2Field2').run()
    std = capsys.readouterr()
    assert std.out == 'Section2Field2Value'


@pytest.mark.usefixtures("op_session")
def test_list(capsys):
    CliSimple('script', 'list').run()
    std = capsys.readouterr()
    assert '\n'.join(sorted(std.out.split('\n'))) == '''
5pwta5jhf5fhj5wzfek4sb22ve Mickaël
a53bppwuhi65b2e34g45fjyfwu Email account
akvb4bbdequd3z6tuorl44btqm Bienvenue dans 1Password !
e25haqmocd5ifiymorfzwxnzry Software licence
hujxh3pryngc7du3owbkwwuh3i test
mvkzp2v2myljdqzxcv5736optu Secure Note
n3iopimevz3pddels3dgfwyp2a Simple Password
ngkzmk54qoltpdoseqspma4tba File certificate
smeg46sk3agiee4cfinvpf7z4u Database
w2euij3m4zhqa5opftnthe5d4q Server
zzfmhu2j7ajq55mmpm3ihs3oqy Connexion'''


@pytest.mark.usefixtures("op_session")
def test_list_custom_field(capsys):
    CliSimple('script', 'list', '--format={uuid} {username} {password}').run()
    std = capsys.readouterr()
    assert '\n'.join(sorted(std.out.split('\n'))) == '''
5pwta5jhf5fhj5wzfek4sb22ve
a53bppwuhi65b2e34g45fjyfwu
akvb4bbdequd3z6tuorl44btqm
e25haqmocd5ifiymorfzwxnzry
hujxh3pryngc7du3owbkwwuh3i
mvkzp2v2myljdqzxcv5736optu
n3iopimevz3pddels3dgfwyp2a  password
ngkzmk54qoltpdoseqspma4tba
smeg46sk3agiee4cfinvpf7z4u username password
w2euij3m4zhqa5opftnthe5d4q username password
zzfmhu2j7ajq55mmpm3ihs3oqy username password'''