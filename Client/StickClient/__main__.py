import json
import argparse
from zipfile import ZipFile
import os
import uuid

from .ipExchange import IpExchange
from .file_transfer import FileTransfer


def zip_folder(folder_path, zip_name, mode='w'):
    """
    Zip a folder, including all it's files.
    :param folder_path: path to folder to be zipped
    :param zip_name: Desired zip file name
    :param mode: Write mode for zip file, see zipfile documentation for details
    """
    with ZipFile(zip_name, mode) as zipfile:
        # Take a walk in the folder and write all paths
        for trip in os.walk(folder_path):
            for _name in trip[2]:
                file_path = os.path.join(trip[0], _name)
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

        file_transfer.send_file(args.target)
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
        file_transfer.receive_file(con_info)
        if con_info['zip'] == "yes":
            print(f'Extracting file: {con_info["filename"]}')
            unzip_file(con_info['filename'])
            print(f'Removing file: {con_info["filename"]}')
            os.remove(con_info['filename'])
