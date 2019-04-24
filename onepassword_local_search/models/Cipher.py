import json


class Cipher:

    iv: str
    data: str
    json: dict
    enc: str

    def __init__(self, json_string):
        self.json = json.loads(json_string)
        self.iv = self.json['iv']
        self.data = self.json['data']
        self.enc = self.json['enc']






