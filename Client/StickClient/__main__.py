import json
import argparse
import sys

from .ipExchange import IpExchange
from .file_transfer import FileTransfer

if __name__ == '__main__':
    # Read config and parse args
    with open('config.json', 'r') as config_file:
        config = json.loads(''.join(config_file.readlines()))

    parser = argparse.ArgumentParser(description="Transfer files over lan")
    parser.add_argument('-p', '--passphrase', type=str, default=None,
                        help='Pass phrase for downloading')
    parser.add_argument('-u', '--upload', help='Set mode to upload',
                        action='store_true', default=False)
    parser.add_argument('-t', '--target', type=str, default=None,
                        help='Target to transmit')
    args = parser.parse_args()

    ip_exchange = IpExchange(config)
    file_transfer = FileTransfer(config)

    if args.upload:
        if not args.target:
            sys.exit('No upload target provided, you must choose what to send')

        passphrase = ip_exchange.send_info()
        print(passphrase)
        print('Sending file...')
        file_transfer.send_file('test.txt')

    elif not args.upload:
        # Request pass phrase and hash it
        if not args.passphrase:
            passphrase = input('Pass phrase: ')
        else:
            passphrase = args.passphrase

        con_info = ip_exchange.get_info(passphrase)
        print(con_info)
        print('Receiving file')
        file_transfer.receive_file(con_info['ip'], con_info['port'],
                                   'test2.txt')

