from json import loads as json_loads


class Cipher:

    iv: str
    data: str
    json: dict
    enc: str

    def __init__(self, json_string):
        self.json = json_loads(json_string)
        self.iv = self.json['iv']
        self.data = self.json['data']
        self.enc = self.json['enc']






