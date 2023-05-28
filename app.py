import os
import uuid
import json
from flask import Flask, request, jsonify
import contracts

app = Flask(__name__)
data_directory = "data"

app = Flask(__name__)


@app.route('/contract', methods=['GET'])
def get_contracts():
    contracts.get_all_contracts()


@app.route('/client/environment/{environment}/{version}', methods=['POST'])
def move_client_version_to_environment(environment, version):
    contracts.move_client_version_to_environment(version, environment)
    contracts.store("data")


@app.route('/server/environment/{environment}/{version}', methods=['POST'])
def set_server_version_for_environment(environment, version):
    contracts.set_server_version_for_environment(version, environment)
    contracts.store("data")


@app.route('/server/environment/{environment}', methods=['GET'])
def get_server_version_for_environment(environment):
    return contracts.get_server_version_for_environment(environment)


@app.route('/client/environment/{environment}', methods=['GET'])
def get_client_versions_in_environment(environment):
    return contracts.get_client_versions_in_environment(environment)


@app.route('/server/validated-contract/{contract}/{version}', methods=['POST'])
def store_server_version_env_info(version):
    pass

@app.route('/client/validated-contract/{contract}/{version}', methods=['POST'])
def store_client_version_env_info(version):
    pass

@app.route('/server/environment/{environment}/{version}', methods=['POST'])
def store_server_version_env_info(environment, version):
    contracts.set_server_version_for_environment(version, environment)
    contracts.store("data")



@app.route('/contract', methods=['POST'])
def upload():
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Invalid JSON data.'}), 400

    contracts.store_contract(contracts.Contract.of(request.get_json()))
    contracts.store("data")


if __name__ == '__main__':
    contracts.load("data")
    app.run(debug=True)
