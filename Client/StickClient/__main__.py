import json
import argparse
from zipfile import ZipFile
import os

from .ipExchange import IpExchange
from .file_transfer import FileTransfer


def zip_folder(folderpath, zipname):
    files = os.listdir(folderpath)
    with ZipFile(zipname, 'w') as zipfile:
        zipfile.write(folderpath)
        for file_path in files:
            file_path = os.path.join(folderpath, file_path)
            print(f'Writing {file_path}')
            zipfile.write(file_path)
        zipfile.close()

if __name__ == '__main__':
    # Read config and parse args
    with open('config.json', 'r') as config_file:
        config = json.loads(''.join(config_file.readlines()))

    parser = argparse.ArgumentParser(description="Transfer files over lan")
    parser.add_argument('-p', '--passphrase', type=str, default=None,
                        help='Pass phrase for downloading')
    parser.add_argument('-t', '--target', type=str, default=None,
                        help='Target to transmit')
    args = parser.parse_args()

    ip_exchange = IpExchange(config)
    file_transfer = FileTransfer(config)

    if args.target:
        passphrase, con_info = ip_exchange.send_info(args.target)
        print(passphrase)
        if not os.path.isfile(args.target):
            print('Compressing folder')
            zip_folder(args.target, 'tmp.zip')
            args.target = 'tmp.zip'

        print('Sending file...')
        file_transfer.send_file(args.target)
        print('Telling server to forget about us.')
        ip_exchange.teardown(con_info['id'])

    elif not args.target:
        # Request pass phrase and hash it
        if not args.passphrase:
            passphrase = input('Pass phrase: ')
        else:
            passphrase = args.passphrase

        con_info = ip_exchange.get_info(passphrase)
        print(con_info)
        file_transfer.receive_file(con_info)

