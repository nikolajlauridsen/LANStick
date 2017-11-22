import json
import argparse
from zipfile import ZipFile
import os

from .ipExchange import IpExchange
from .file_transfer import FileTransfer


def zip_folder(folder_path, zip_name, mode='w'):
    """
    Zip a folder, including all it's files.
    :param folder_path: path to folder to be zipped
    :param zip_name: Desired zip file name
    :param mode: Write mode for zip file, see zipfile documentation for details
    """
    files = []
    for trip in os.walk(folder_path):
        for _name in trip[2]:
            files.append(os.path.join(trip[0], _name))

    with ZipFile(zip_name, mode) as zipfile:
        zipfile.write(folder_path)
        for file_path in files:
            print(f'Writing {file_path}')
            zipfile.write(file_path)
        zipfile.close()


def unzip_file(zip_path):
    with ZipFile(zip_path, 'r') as zipfile:
        zipfile.extractall()
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
        _zip = 'no'
        if os.path.isdir(args.target):
            print('Compressing folder')
            zip_folder(args.target, 'tmp.zip')
            args.target = 'tmp.zip'
            _zip = 'yes'

        passphrase, con_info = ip_exchange.send_info(args.target, _zip=_zip)
        print(passphrase)

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
        if con_info['zip'] == "yes":
            unzip_file(con_info['filename'])
