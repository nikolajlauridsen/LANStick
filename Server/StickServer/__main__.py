import sys
import json
from flask import Flask, request

stick_server = Flask(__name__)

# List of dictionaries containing connection info
# this is probably not a good data model, but good enough for now
con_info = []


@stick_server.route('/transfer', methods=['GET', 'POST'])
def transfer():
    """
    Endpoint for sharing and retrieving connection data
    """
    if request.method == 'POST':
        # Store connection info
        return "Not yet implemented"

    if request.method == 'GET':
        # Retrieve connection info
        return "Not yet implemented"


@stick_server.route('/teardown', methods=['POST'])
def teardown():
    """
    Transfer complete, remove connection info
    :return:
    """
    return "Not yet implemented"


if __name__ == '__main__':
    # Read config from file
    with open('server_info.json', 'r') as config_file:
        config = json.loads(''.join(config_file.readlines()))

    try:
        stick_server.run(host=config['host'],
                         port=int(config['port']),
                         debug=True)
    except ValueError:
        sys.exit('Bad config file, stopping')
