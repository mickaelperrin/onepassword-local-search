from onepassword_local_search.models.Cipher import Cipher


class Item:

    id: str
    uuid: str
    vault_id: str
    overview: Cipher
    details: Cipher

    def __init__(self, row):
        self.id = row['id']
        self.uuid = row['uuid']
        self.vault_id = row['vault_id']
        self.overview = Cipher(row['overview'])
        self.details = Cipher(row['details'])

