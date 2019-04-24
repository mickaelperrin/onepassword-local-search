from onepassword_local_search.models.Cipher import Cipher


class Item:

    id: str
    uuid: str
    vault_id: str
    encryptedOverview: Cipher
    encryptedDetails: Cipher
    overview: dict
    details: dict

    def __init__(self, row):
        self.id = row['id']
        self.uuid = row['uuid']
        self.vaultId = row['vault_id']
        self.encryptedOverview = Cipher(row['overview'])
        self.encryptedDetails = Cipher(row['details'])

