import requests
import serialization


class OutgoingHandler:
    def __init__(self, address: str, port: int):
        self._url = "http://{}:{}".format(address, port)

    def send(self, data):
        try:
            res = requests.post(self._url, serialization.serialize(data))
        except requests.exceptions.ConnectionError:
            return False, None
        return res.ok, serialization.deserialize(res.content)