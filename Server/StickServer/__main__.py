import sys
import json
from flask import Flask, request, jsonify, abort

stick_server = Flask(__name__)

# List of dictionaries containing connection info
# this is probably not a good data model, but good enough for now
info_list = []


@stick_server.route('/transfer', methods=['GET', 'POST'])
def transfer():
    """
    Endpoint for sharing and retrieving connection data
    """
    if request.method == 'POST':
        # TODO: validate form fields
        con_info = {"id": request.form['id'],
                    "ip": request.form['ip'],
                    "port": int(request.form['port']),
                    "filename": request.form['filename'],
                    "zip": request.form['zip'],
                    "size": request.form['size']}
        info_list.append(request.form)
        return "Connection data saved"

    if request.method == 'GET':
        # Retrieve connection info
        for con_data in info_list:
            if con_data['id'] == request.form['id']:
                return jsonify(con_data)
        # No data found bad request
        return abort(400)


@stick_server.route('/teardown', methods=['POST'])
def teardown():
    """
    Transfer complete, remove connection info
    :return:
    """
    for con_data in info_list:
        if con_data['id'] == request.form['id']:
            info_list.remove(con_data)
            return "Connection data removed"
    return abort(404)


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
