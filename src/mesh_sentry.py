import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Service:
    name: str
    namespace: str
    health: str
    traffic: int

class MeshSentry:
    def __init__(self):
        self.services = []

    def add_service(self, service: Service):
        self.services.append(service)

    def filter_services(self, name: str = None, namespace: str = None) -> List[Service]:
        filtered_services = self.services
        if name:
            filtered_services = [s for s in filtered_services if s.name == name]
        if namespace:
            filtered_services = [s for s in filtered_services if s.namespace == namespace]
        return filtered_services

    def get_service_health(self, name: str) -> str:
        for service in self.services:
            if service.name == name:
                return service.health
        return None

    def get_service_traffic(self, name: str) -> int:
        for service in self.services:
            if service.name == name:
                return service.traffic
        return None

    def visualize_mesh(self) -> Dict:
        mesh_data = {}
        for service in self.services:
            mesh_data[service.name] = {
                'namespace': service.namespace,
                'health': service.health,
                'traffic': service.traffic
            }
        return mesh_data
