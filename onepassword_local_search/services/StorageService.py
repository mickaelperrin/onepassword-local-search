from os import environ, path as os_path
import sqlite3


class StorageService:

    app_path: str
    con: sqlite3.Connection
    cur: sqlite3.Cursor

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
        return self.cur.execute(query).fetchone()

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
        path = self.guess_database_dir()
        if not os_path.isfile(path):
            raise Exception('Database file not found at ' + path)
        con = sqlite3.connect(path)
        con.row_factory = self._dict_factory
        return con

