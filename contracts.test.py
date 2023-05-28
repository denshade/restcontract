import contracts
import unittest

ENVIRONMENT = "dev"

CLIENT_VERSION = "client_1"

SERVER_VERSION = "server_1"


class AppTestCase(unittest.TestCase):

    def setUp(self):
        contracts.clear()

    #   -> There are no clients.
    #   -> check server can install on environment.
    #   It can.
    def test_check_server_can_deploy_if_no_clients_in_env(self):
        contract = contracts.Contract([])
        contract_hash = contracts.store_contract(contract)
        contracts.link_server_version_contract(contract_hash, SERVER_VERSION)
        self.assertTrue(contracts.check_server_can_move_to_environment(SERVER_VERSION, ENVIRONMENT))

    #    -> set 1 contract a version of server
    #    -> DO NOT confirm client can handle contract
    #    -> move client to environment
    #    -> check server can install on environment.
    #   It cannot.
    def test_cannot_deploy_if_clients_not_proven(self):
        contract = contracts.Contract([])
        contracts.store_contract(contract)
        contracts.link_server_version_contract(contract, SERVER_VERSION)
        contracts.move_client_version_to_environment(CLIENT_VERSION, ENVIRONMENT)
        self.assertFalse(contracts.check_server_can_move_to_environment(SERVER_VERSION, ENVIRONMENT))

    #    -> set 1 contract a version of server
    #    -> confirm client can handle contract
    #    -> move client to environment
    #    -> check server can install on environment.
    #   It can.
    def test_can_deploy_new_server_if_client_proven_and_server_proven(self):
        contract = contracts.Contract([])
        contract_hash = contracts.store_contract(contract)
        contracts.link_server_version_contract(contract, SERVER_VERSION)
        contracts.link_client_version_can_handle_contract(contract_hash, CLIENT_VERSION)
        contracts.move_client_version_to_environment(CLIENT_VERSION, ENVIRONMENT)
        self.assertTrue(contracts.check_server_can_move_to_environment(SERVER_VERSION, ENVIRONMENT))

    #    -> set 1 contract a version of server
    #    -> move version to environment.
    #    -> confirm client can handle contract
    #    -> check client can install on environment.
    #   It can.
    def test_can_deploy_new_client_if_server_proven(self):
        contract = contracts.Contract([])
        contract_hash = contracts.store_contract(contract)
        contracts.link_server_version_contract(contract, SERVER_VERSION)
        contracts.set_server_version_for_environment(SERVER_VERSION, ENVIRONMENT)
        contracts.link_client_version_can_handle_contract(contract_hash, CLIENT_VERSION)
        self.assertTrue(contracts.check_client_can_move_to_environment(CLIENT_VERSION, ENVIRONMENT))

    #    -> set 1 contract a version of server
    #    -> move version to environment.
    #    -> DO NOT confirm client can handle contract
    #    -> check client can install on environment.
    #    It cannot.
    def test_cannot_deploy_new_client_if_client_not_proven(self):
        contract = contracts.Contract([])
        contract_hash = contracts.store_contract(contract)
        contracts.link_server_version_contract(contract, SERVER_VERSION)
        contracts.set_server_version_for_environment(SERVER_VERSION, ENVIRONMENT)
        self.assertFalse(contracts.check_client_can_move_to_environment(CLIENT_VERSION, ENVIRONMENT))


if __name__ == '__main__':
    unittest.main()
