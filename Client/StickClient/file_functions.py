import socket
import os
from zipfile import ZipFile

from .PyCLIBar.CLIBar import CLIBar
from .config import listening_port

BUFFSIZE = 1024*4


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


def send_file(filepath):
    # Establish connection
    print('Creating socket.')
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(('0.0.0.0', listening_port,))

    print('Awaiting connection')
    listen_socket.listen()
    connection, address = listen_socket.accept()

    print('Sending file')
    with open(filepath, 'rb') as _file:
        connection.sendfile(_file)
    print('Done! Closing connection')
    connection.close()


def receive_file(con_info):
    if os.path.isfile(con_info['filename']):
        response = input(f'A file with the name {con_info["filename"]} '
                         f'already exists\nWant to rename? y/n: ')
        if response.strip().lower() == 'y':
            con_info['filename'] = input('Filename: ')

    # Establish connection
    print('Creating connection')
    sending_connection = socket.create_connection((con_info["ip"],
                                                   con_info["port"]))

    print('Receiving file')
    # Receiving file
    bar = CLIBar(_max=int(con_info['size']))
    with open(con_info["filename"], 'wb') as _file:
        bar.start()
        count = 0
        while True:
            data = sending_connection.recv(BUFFSIZE)
            if not data:
                break

            _file.write(data)
            if count == 500:
                print(bar.get_bar(), end='\r')
                count = 0
            bar.step(len(data))
            count += 1
    print('Done! Closing connection')
    sending_connection.close()
