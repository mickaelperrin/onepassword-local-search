from os import environ, path as os_path
from sqlite3 import Connection, Cursor, connect as sqlite3_connect
from onepassword_local_search.exceptions.ManagedException import ManagedException


class StorageService:

    app_path: str
    con: Connection
    cur: Cursor

    def __init__(self):
        self.con = self.set_database_connexion()
        self.cur = self.con.cursor()

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_item_by_uuid(self, uuid):
        query = "SELECT * FROM items WHERE uuid = '%s'" % uuid
        res = self.cur.execute(query).fetchone()
        if res is None:
            raise ManagedException('Unable to find item with uuid: %s' % uuid)
        return res

    @staticmethod
    def guess_database_dir():
        if environ.get('ONEPASSWORD_LOCAL_DATABASE_PATH'):
            path = environ.get('ONEPASSWORD_LOCAL_DATABASE_PATH')
        else:
            path = None

        if path is not None and path != '':
            return path
        else:
            raise Exception('Unable to determine 1Password local database path')

    def set_database_connexion(self):
        path = os_path.expandvars(self.guess_database_dir())
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