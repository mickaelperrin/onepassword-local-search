from onepassword_local_search.models.Cipher import Cipher
from json import dumps as json_dumps
from onepassword_local_search.exceptions.ManagedException import ManagedException


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

    def get(self, field=None):
        if field is None:
            self.__delattr__('encryptedOverview')
            self.__delattr__('encryptedDetails')
            return self.output(self.__dict__)

        path = field.split(';;')
        out = None

        if field in ['title', 'url']:
            out = self.overview.get(field)
        elif field in ['username', 'password']:
            out = self._get_details_field(field)
        elif field == 'notesPlain':
            out = self.details.get(field)
        elif hasattr(self, field):
            out = self.__getattribute__(field)
        elif path != field:
            for section in self.details.get('sections'):
                if section['title'] == path[0]:
                    for f in section['fields']:
                        if f['t'] == path[1]:
                            out = f['v']
                            break

        if not out:
            raise ManagedException('Unable to find field %s of item %s ' % (field, self.uuid))

        return self.output(out)

    def _get_details_field(self, field):
        for f in self.details.get('fields'):
            if f['name'] == field:
                return f['value']
        return None

    def output(self, content):
        out_type = type(content).__name__
        if out_type in ['str', 'int']:
            return content
        else:
            return json_dumps(content)