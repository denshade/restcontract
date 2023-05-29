# Rest Contract
This tool allows a simple contract testing framework. 
The workflow is very simple.

## Concepts
* A client or consumer that will consume the API for which we define contracts.
* A contract defines one URL, one body and headers
* A provider which will host the API
* A validated contract is a contract for which on a specific client version or server version tests have proven they can handle the contract.
* An environment, e.g. development/production where software is run. 
* Deployed contracts, is a set of contracts that are active on a provider in a specific environment.

## Workflow
### Uploading contracts
1. A client or provider can define a contract and upload it to the rest contract server.
### Marking versions compatible with a contract 
A client or provider can retrieve a contract and run a test against the contract url and expected response body and headers.  
For a client this is usually done by mocking the provider and running a unit test.
For a provider state is initialized and a request is triggered. Only if the response is identical to the contract response it is marked as compatible.

<b> A version is said to be compatible with a contract if a test has succeeded and marked it as compatible with the rest contract server.</b> 

### Deploying safely

Deploying safely is different depending on what is being deployed.

#### Deploying a new consumer
A deployed provider version is compatible with a set of contracts. The contract server can be queried for those.
Before a client can be safely deployed it should confirm its version is compatible with the deployed contracts.

#### Deploying a new provider
Given a group of clients that are deployed. These deployed clients have a set of client versions. 
Before a new provider can be deployed it must have confirmed for each of the deployed client contracts it can handle them correctly.

## Endpoints

POST /contract

Post a contract

body: 
```
{
 url: "/blog",
 method: "POST",
 body: {},
 state: "noblogs",
 response: {
   headers: {status: "204"}
   body: "OK"
 }
}
```
required

GET /contract
Gets all contracts.