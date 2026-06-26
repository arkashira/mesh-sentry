import json
from dataclasses import dataclass
from typing import Dict, List
import time
import random

@dataclass
class Node:
    name: str
    error_rate: float
    latency: float

@dataclass
class Connection:
    source: str
    target: str
    traffic: int

class MeshSentry:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.connections: Dict[str, Connection] = {}

    def add_node(self, name: str, error_rate: float, latency: float):
        self.nodes[name] = Node(name, error_rate, latency)

    def add_connection(self, source: str, target: str, traffic: int):
        self.connections[f"{source}-{target}"] = Connection(source, target, traffic)

    def get_topology(self):
        topology = {"nodes": [], "connections": []}
        for node in self.nodes.values():
            topology["nodes"].append({"name": node.name, "error_rate": node.error_rate, "latency": node.latency})
        for connection in self.connections.values():
            topology["connections"].append({"source": connection.source, "target": connection.target, "traffic": connection.traffic})
        return topology

    def update_traffic(self):
        for connection in self.connections.values():
            connection.traffic = random.randint(0, 100)

    def get_traffic_flow(self):
        traffic_flow = {}
        for connection in self.connections.values():
            traffic_flow[f"{connection.source}-{connection.target}"] = connection.traffic
        return traffic_flow

    def get_error_rates(self):
        error_rates = {}
        for node in self.nodes.values():
            error_rates[node.name] = node.error_rate
        return error_rates

    def get_latency(self):
        latency = {}
        for node in self.nodes.values():
            latency[node.name] = node.latency
        return latency
