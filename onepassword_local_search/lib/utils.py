from uuid import UUID
import string


def is_uuid(uuid_string, version=4):
    try:
        uid = UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False


class SimpleFormatter(string.Formatter):
    output_encoding: str = None

    def __init__(self, output_encoding=None):
        super().__init__()
        self.output_encoding = output_encoding

    def get_value(self, key, args, kwargs):
        item = args[0]
        result = item.get(key, strict=False)
        if result is not None and self.output_encoding == 'json':
            import json
            return json.dumps(result)[1:-1]
        else:
            return result
