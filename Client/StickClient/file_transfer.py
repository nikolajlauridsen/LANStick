import socket
import os

from .PyCLIBar.CLIBar import CLIBar
from .config import listening_port


class FileTransfer:
    def __init__(self):
        self.buffsize = 1024*4

    def send_file(self, filepath):
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

    def receive_file(self, con_info):
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
                data = sending_connection.recv(self.buffsize)
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
