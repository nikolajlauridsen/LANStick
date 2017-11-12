import json
import argparse

from .ipExchange import IpExchange

if __name__ == '__main__':
    # Read config and parse args
    with open('config.json', 'r') as config_file:
        config = json.loads(''.join(config_file.readlines()))

    ip = config["server_ip"]
    port = config["server_port"]
    url = f"http://{ip}:{port}/transfer"

    parser = argparse.ArgumentParser(description="Transfer files over lan")
    parser.add_argument('-p', '--passphrase', type=str, default=None,
                        help='Pass phrase for downloading')
    parser.add_argument('-u', '--upload', help='Set mode to upload',
                        action='store_true', default=False)
    args = parser.parse_args()

    ip_exchange = IpExchange(config)

    if args.upload:
        passphrase = ip_exchange.send_info()
        print(passphrase)

    elif not args.upload:
        # Request pass phrase and hash it
        if not args.passphrase:
            passphrase = input('Pass phrase: ')
        else:
            passphrase = args.passphrase

        con_info = ip_exchange.get_info(passphrase)
        print(con_info)
