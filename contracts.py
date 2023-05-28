from typing import Dict, Any
import os
import json


class ContractLine:
    url = ""
    expected_json = ""
    expected_headers = ""

    def __init__(self, url, expected_json, expected_headers):
        self.url = url
        self.expected_headers = expected_headers
        self.expected_json = expected_json


class Contract:
    contract_lines = []

    def __init__(self, contract_lines):
        self.contract_lines = contract_lines


stored_contracts = {}
supported_version_to_contract_hash_set_clients = {}
client_contracts_in_environment = {}
server_version_to_contract: Dict[Any, Any] = {}
server_version_in_environment = {}


# contract retrieval

def store_contract(contract):
    stored_contracts[hash(contract)] = contract
    return hash(contract)


def get_contract_for(contract_hash):
    return stored_contracts[contract_hash]


def get_contract_for_server_version(server_version):
    if server_version not in server_version_to_contract:
        raise FileNotFoundError(f"{server_version} not found")
    return server_version_to_contract[server_version]


## linking

# setting
def link_client_version_can_handle_contract(contract_hash, client_version):
    if client_version not in supported_version_to_contract_hash_set_clients:
        supported_version_to_contract_hash_set_clients[client_version] = set()
    supported_version_to_contract_hash_set_clients[client_version].add(contract_hash)


def link_server_version_contract(contract, server_version):
    server_version_to_contract[server_version] = contract


# checking


def check_client_can_handle(contract_hash, client_version):
    if client_version not in supported_version_to_contract_hash_set_clients:
        return False
    return client_version in supported_version_to_contract_hash_set_clients and contract_hash in \
           supported_version_to_contract_hash_set_clients[
               client_version]


## environment functions
# setting

def move_client_version_to_environment(client_version, environment):
    if environment not in client_contracts_in_environment:
        client_contracts_in_environment[environment] = set()
    client_contracts_in_environment[environment].add(client_version)


def set_server_version_for_environment(server_version, environment):
    server_version_in_environment[environment] = server_version


# getting


def get_client_versions_in_environment(environment):
    if environment in client_contracts_in_environment:
        return client_contracts_in_environment[environment]
    else:
        return []


def get_server_version_for_environment(environment):
    if environment not in server_version_in_environment:
        return None
    return server_version_in_environment[environment]


# checking


def check_server_can_move_to_environment(server_version, environment):
    # only if the clients in the environment can handle the new contract
    contract = get_contract_for_server_version(server_version)
    client_versions = get_client_versions_in_environment(environment)
    if len(client_versions) == 0:
        return True
    supported_clients = [check_client_can_handle(hash(contract), client_version) for client_version in
                         client_versions]
    return all(supported_clients)


def check_client_can_move_to_environment(client_version, environment):
    server_version = get_server_version_for_environment(environment)
    contract = get_contract_for_server_version(server_version)
    return check_client_can_handle(hash(contract), client_version)


# manipulation of contracts and data.
def clear():
    stored_contracts.clear()
    supported_version_to_contract_hash_set_clients.clear()
    client_contracts_in_environment.clear()


def store(base_path):
    # stored_contracts
    stored_contracts_file = os.path.join(base_path, 'stored_contracts.json')
    with open(stored_contracts_file, 'w') as file:
        json.dump(stored_contracts, file)

    # supported_version_to_contract_hash_set_clients
    supported_version_to_contract_hash_set_clients_file = os.path.join(base_path,
                                                                       'supported_version_to_contract_hash_set_clients.json')
    with open(supported_version_to_contract_hash_set_clients_file, 'w') as file:
        json.dump(supported_version_to_contract_hash_set_clients, file)

    # client_contracts_in_environment
    client_contracts_in_environment_file = os.path.join(base_path, 'client_contracts_in_environment.json')
    with open(client_contracts_in_environment_file, 'w') as file:
        json.dump(client_contracts_in_environment, file)

    # server_version_to_contract
    server_version_to_contract_file = os.path.join(base_path, 'server_version_to_contract.json')
    with open(server_version_to_contract_file, 'w') as file:
        json.dump(server_version_to_contract, file)

    # server_version_in_environment
    server_version_in_environment_file = os.path.join(base_path, 'server_version_in_environment.json')
    with open(server_version_in_environment_file, 'w') as file:
        json.dump(server_version_in_environment, file)


def load_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return None


def load(base_path):
    global stored_contracts
    global supported_version_to_contract_hash_set_clients
    global client_contracts_in_environment
    global server_version_to_contract
    global server_version_in_environment

    # stored_contracts
    stored_contracts_file = os.path.join(base_path, 'stored_contracts.json')
    stored_contracts = load_json_file(stored_contracts_file)

    # supported_version_to_contract_hash_set_clients
    supported_version_to_contract_hash_set_clients_file = os.path.join(base_path,
                                                                       'supported_version_to_contract_hash_set_clients.json')
    supported_version_to_contract_hash_set_clients = load_json_file(supported_version_to_contract_hash_set_clients_file)

    # client_contracts_in_environment
    client_contracts_in_environment_file = os.path.join(base_path, 'client_contracts_in_environment.json')
    client_contracts_in_environment = load_json_file(client_contracts_in_environment_file)

    # server_version_to_contract
    server_version_to_contract_file = os.path.join(base_path, 'server_version_to_contract.json')
    server_version_to_contract = load_json_file(server_version_to_contract_file)

    # server_version_in_environment
    server_version_in_environment_file = os.path.join(base_path, 'server_version_in_environment.json')
    server_version_in_environment = load_json_file(server_version_in_environment_file)
