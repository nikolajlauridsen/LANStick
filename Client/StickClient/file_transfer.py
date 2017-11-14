import socket


class FileTransfer:
    def __init__(self, config):
        self.config = config
        self.buffsize = 4063

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

    def receive_file(self, host, port, filename):
        # Establish connection
        print('Creating connection')
        sending_connection = socket.create_connection((host, port))

        print('Receiving file')
        # Receiving file
        with open(filename, 'wb') as _file:
            while True:
                data = sending_connection.recv(self.buffsize)
                if not data:
                    break
                _file.write(data)
        print('Done! Closing connection')
        sending_connection.close()
