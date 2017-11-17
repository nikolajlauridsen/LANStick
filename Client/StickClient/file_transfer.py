import socket

from .PyCLIBar.CLIBar import CLIBar


class FileTransfer:
    def __init__(self, config):
        self.config = config
        self.buffsize = 1024*4

    def send_file(self, filepath):
        # Establish connection
        print('Creating socket.')
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(('0.0.0.0', int(self.config['listening_port']),))

        print('Awaiting connection')
        listen_socket.listen()
        connection, address = listen_socket.accept()

        print('Sending file')
        with open(filepath, 'rb') as _file:
            connection.sendfile(_file)
        print('Done! Closing connection')
        connection.close()

    def receive_file(self, con_info):
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
                if count == 100:
                    print(bar.get_bar(), end='\r')
                    count = 0
                bar.step(len(data))
                count += 1
        print('Done! Closing connection')
        sending_connection.close()
