import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Service:
    name: str
    performance_metrics: Dict[str, float]

class MeshSentry:
    def __init__(self):
        self.services = {}

    def add_service(self, service: Service):
        self.services[service.name] = service

    def get_service_topology(self) -> Dict[str, List[str]]:
        topology = {}
        for service_name, service in self.services.items():
            topology[service_name] = list(self.services.keys())
        return topology

    def update_service_performance_metrics(self, service_name: str, metrics: Dict[str, float]):
        if service_name in self.services:
            self.services[service_name].performance_metrics = metrics
        else:
            raise ValueError("Service not found")

    def get_service_performance_metrics(self, service_name: str) -> Dict[str, float]:
        if service_name in self.services:
            return self.services[service_name].performance_metrics
        else:
            raise ValueError("Service not found")
