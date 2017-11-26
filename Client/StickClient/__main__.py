import argparse
import os
import uuid

from .ipExchange import IpExchange
from .file_functions import send_file, receive_file, zip_folder, unzip_file


def main():
    # Parse args
    parser = argparse.ArgumentParser(description="Transfer files over lan")
    parser.add_argument('-p', '--passphrase', type=str, default=None,
                        help='Pass phrase for downloading')
    parser.add_argument('-t', '--target', type=str, default=None,
                        help='Target to transmit')
    args = parser.parse_args()

    ip_exchange = IpExchange()

    if args.target:
        _zip = 'no'
        zip_name = None
        if os.path.isdir(args.target):
            print(f' Compressing {args.target} '.center(80, '='))
            zip_name = f"{str(uuid.uuid4())}.zip"
            zip_folder(args.target, zip_name)
            args.target = zip_name
            _zip = 'yes'
            print(f' Folder compressed to: {zip_name} '.center(80, '='))

        passphrase, con_info = ip_exchange.send_info(args.target, _zip=_zip)
        print(f'\nPassphrase: {passphrase}')

        send_file(args.target)
        print('Telling server to forget about us.')
        ip_exchange.teardown(con_info['id'])
        if _zip == 'yes' and zip_name:
            print(f'Removing file {zip_name}')
            os.remove(zip_name)

    elif not args.target:
        # Request pass phrase and hash it
        if not args.passphrase:
            passphrase = input('Pass phrase: ')
        else:
            passphrase = args.passphrase

        con_info = ip_exchange.get_info(passphrase)
        receive_file(con_info)
        if con_info['zip'] == "yes":
            print(f'Extracting file: {con_info["filename"]}')
            unzip_file(con_info['filename'])
            print(f'Removing file: {con_info["filename"]}')
            os.remove(con_info['filename'])


if __name__ == '__main__':
    main()
