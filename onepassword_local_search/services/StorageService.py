from os import environ, path as os_path
from sqlite3 import Connection, Cursor, connect as sqlite3_connect
from onepassword_local_search.exceptions.ManagedException import ManagedException
from platform import system


class StorageService:

    app_path: str
    con: Connection
    cur: Cursor
    uuid_mapping_table_name: str = 'uuid_mapping'
    use_custom_uuid_mapping: bool = False

    def __init__(self, use_custom_uuid_mapping=False):
        self.use_custom_uuid_mapping = use_custom_uuid_mapping
        self.con = self.set_database_connexion()
        self.cur = self.con.cursor()
        if use_custom_uuid_mapping:
            self.checks_for_uuid_mapping()

    def checks_for_uuid_mapping(self):
        if not self._has_table(StorageService.uuid_mapping_table_name):
            self.create_uuid_mapping_table()

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _has_table(self, table_name):
        query = "SELECT name from sqlite_master WHERE type='table' AND name='%s';" % table_name
        return self.con.execute(query).fetchone()

    def create_uuid_mapping_table(self):
        request = """
                    BEGIN;
                    CREATE TABLE IF NOT EXISTS %s (                        
                        op_uuid TEXT,
                        custom_uuid TEXT,
                        PRIMARY KEY (op_uuid, custom_uuid),
                        FOREIGN KEY (op_uuid) REFERENCES items (uuid)
                        ON DELETE CASCADE
                    );
                    CREATE INDEX idx_%s_custom_uuid ON %s (custom_uuid);
                    COMMIT;
                  """ % (StorageService.uuid_mapping_table_name, StorageService.uuid_mapping_table_name, StorageService.uuid_mapping_table_name)
        return self.con.executescript(request)

    def truncate_uuid_mapping_table(self):
        request = """
                    BEGIN;
                    DELETE FROM uuid_mapping; 
                    COMMIT;
                  """
        return self.con.executescript(request)

    def uuid_mapping_has_entries(self):
        query = "SELECT COUNT(custom_uuid) as nb FROM %s" % StorageService.uuid_mapping_table_name
        return self.cur.execute(query).fetchone()['nb']

    def get_item_by_uuid(self, uuid, use_custom_uuid_mapping=False):
        if use_custom_uuid_mapping:
            query = "SELECT * FROM items WHERE uuid = (SELECT op_uuid FROM %s WHERE custom_uuid='%s')" % (StorageService.uuid_mapping_table_name, uuid)
        else:
            query = "SELECT * FROM items WHERE uuid = '%s'" % uuid
        res = self.cur.execute(query).fetchone()
        if res is None:
            raise ManagedException('Unable to find item with uuid: %s' % uuid)
        return res

    def list_mapping(self):
        query = "SELECT * FROM %s;" % StorageService.uuid_mapping_table_name
        return self.cur.execute(query).fetchall()

    def add_uuid_mapping(self, custom_uuid, op_uuid):
        request = "INSERT INTO %s VALUES ('%s','%s')" % (StorageService.uuid_mapping_table_name, op_uuid, custom_uuid)
        return self.cur.execute(request)

    @staticmethod
    def guess_database_path():
        if environ.get('ONEPASSWORD_LOCAL_DATABASE_PATH'):
            path = environ.get('ONEPASSWORD_LOCAL_DATABASE_PATH')
        elif system() == 'Darwin':
            path = os_path.join(environ.get('HOME'), 'Library', 'Group Containers', '2BUA8C4S2C.com.agilebits', 'Library', 'Application Support', '1Password', 'Data', 'B5.sqlite')
        elif system() == 'Windows':
            path = os_path.join(environ.get('LocalAppData'), '1password', 'data', '1Password10.sqlite')
        else:
            path = None

        if path is not None and path != '':
            return path
        else:
            raise Exception('Unable to determine 1Password local database patsh')

    def set_database_connexion(self):
        path = os_path.expandvars(self.guess_database_path())
        if not os_path.isfile(path):
            raise Exception('Database file not found at ' + path)
        con = sqlite3_connect(path)
        con.row_factory = self._dict_factory
        return con

    def get_account_id_from_user_uuid(self, user_uuid):
        query = "select id from accounts where user_uuid='%s';" % user_uuid
        return self.cur.execute(query).fetchone()['id']

    def get_encrypted_symmetric_key(self, account_id):
        query = "select enc_sym_key from keysets where encrypted_by='mp' and account_id=%s;" % account_id
        return self.cur.execute(query).fetchone()['enc_sym_key']

    def get_account_key(self, account_id):
        query = "select enc_login from accounts where id=%s" % account_id
        return self.cur.execute(query).fetchone()['enc_login']

    def get_encrypted_private_key(self, account_id):
        query = "select enc_pri_key from keysets where encrypted_by='mp' and account_id=%s;" % account_id
        return self.cur.execute(query).fetchone()['enc_pri_key']

    def get_encrypted_vault_key(self, vault_id, account_id):
        query = "select enc_vault_key from vault_access where id=%s and account_id=%s;" % (vault_id, account_id)
        return self.cur.execute(query).fetchone()['enc_vault_key']

    def list(self):
        query = "select * from items where trashed = 0"
        return self.cur.execute(query).fetchall()