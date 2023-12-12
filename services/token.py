import json

from typing import Dict
from jose import jwt


class Token:
    def __init__(self, key: str):
        self.__secret_key = key

    def create(self, subject: Dict) -> str:
        claims = {'sub': json.dumps(subject)}

        return jwt.encode(claims, self.__secret_key)

    def get_subject(self, token: str) -> Dict:
        claims = jwt.decode(token, self.__secret_key)

        return json.loads(claims['sub'])
