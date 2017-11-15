from random_words import RandomWords, RandomNicknames
import requests
import socket
import hashlib
import json
import os


class IpExchange:
    def __init__(self, config):
        self.config = config
        self.sever_url = f'http://{config["server_ip"]}:{config["server_port"]}'

        self.rw = RandomWords()
        self.rn = RandomNicknames()

    def send_info(self, filename):
        filename = os.path.split(filename)[-1]

        # Get connection info
        ip = self.get_local_ip()

        # Generate pass phrase
        passphrase = f"{self.rn.random_nick(gender='u').capitalize()}{self.rw.random_word().capitalize()}"
        # Hash it
        pass_hash = hashlib.md5(passphrase.encode()).hexdigest()

        # Send it off to the server
        payload = {"id": pass_hash,
                   "filename": filename,
                   "ip": ip,
                   "port": self.config["listening_port"]}
        res = requests.post(f'{self.sever_url}/transfer', data=payload)
        res.raise_for_status()
        return passphrase

    def get_info(self, passphrase):
        # Request pass phrase and hash it
        pass_hash = hashlib.md5(passphrase.encode()).hexdigest()

        # Request ip and port from server
        payload = {"id": pass_hash}
        res = requests.get(f'{self.sever_url}/transfer', data=payload)
        res.raise_for_status()
        return json.loads(res.content.decode())

    @staticmethod
    def get_local_ip():
        """
        Get the local IP
        Thanks stackoverflow
        https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/25850698#25850698
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]

