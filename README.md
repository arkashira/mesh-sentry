# Mesh Sentry

Mesh Sentry is a real-time traffic visualization dashboard for service mesh traffic flows.

## Features

* Displays service mesh topology with nodes and connections
* Traffic flow visualization updates every 2 seconds
* Error rates and latency metrics are clearly displayed on nodes

## Usage

1. Install the required dependencies using `poetry install`
2. Run the tests using `pytest`
3. Use the `MeshSentry` class to create a new instance and add nodes and connections
4. Use the `get_topology`, `get_traffic_flow`, `get_error_rates`, and `get_latency` methods to retrieve the relevant data
