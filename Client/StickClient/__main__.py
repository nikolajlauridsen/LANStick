import sys
import requests
import socket
import hashlib
import json
import argparse
from random_words import RandomWords, RandomNicknames


def get_ip():
    """
    Get the local IP
    Thanks stackoverflow
    https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/25850698#25850698
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    return s.getsockname()[0]


if __name__ == '__main__':
    # Read config and parse args
    with open('config.json', 'r') as config_file:
        config = json.loads(''.join(config_file.readlines()))

    ip = config["server_ip"]
    port = config["server_port"]
    url = f"http://{ip}:{port}/transfer"

    parser = argparse.ArgumentParser(description="Transfer files over lan")
    parser.add_argument('-u', '--upload', help='Set mode to upload', action='store_true', default=False)
    args = parser.parse_args()

    if args.upload:
        # Get connection info
        ip = get_ip()
        port = config['listening_port']

        # Generate pass phrase
        rw = RandomWords()
        rn = RandomNicknames()
        passphrase = f"{rn.random_nick(gender='u').capitalize()}{rw.random_word().capitalize()}"
        # Hash it
        pass_hash = hashlib.md5(passphrase.encode()).hexdigest()
        print(f"ip: {ip}\nport: {port}\npass phrase: {passphrase}\nhash: {pass_hash}")

        # Send it off to the server
        payload = {"id": pass_hash,
                   "ip": ip,
                   "port": port}
        res = requests.post(url, data=payload)
        print(f"Code:{res.status_code}\n{res.content}")

    elif not args.upload:
        # Request pass phrase and hash it
        passphrase = input('Pass phrase: ')
        pass_hash = hashlib.md5(passphrase.encode()).hexdigest()
        print(f'Hashed pass phrase: {pass_hash}')

        # Request ip and port from server
        payload = {"id": pass_hash}
        res = requests.get(url, data=payload)
        print(f"Code:{res.status_code}\n{res.content.decode()}")
