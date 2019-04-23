from os import environ, path as os_path
import sqlite3


class StorageService:

    app_path: str
    db: sqlite3.Connection

    def __init__(self, database_path=None):
        self.db = self.set_database_connexion(database_path)

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

    def set_database_connexion(self, path):
        if path is None:
            path = self.guess_database_dir()
        if not os_path.isfile(path):
            raise Exception('Database file not found at ' + path)
        return sqlite3.connect(path)
