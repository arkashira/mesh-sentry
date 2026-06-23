import json
from dataclasses import dataclass
from typing import List

@dataclass
class Policy:
    name: str
    rules: List[str]

@dataclass
class Alert:
    policy_name: str
    message: str

class MeshSentry:
    def __init__(self):
        self.policies = []
        self.alerts = []

    def add_policy(self, policy: Policy):
        self.policies.append(policy)

    def add_alert(self, alert: Alert):
        self.alerts.append(alert)

    def enforce_policies(self, service_communication: str) -> List[Alert]:
        triggered_alerts = []
        for policy in self.policies:
            for rule in policy.rules:
                if rule in service_communication:
                    triggered_alerts.append(Alert(policy.name, f"Policy {policy.name} triggered"))
        return triggered_alerts

    def get_alerts(self) -> List[Alert]:
        return self.alerts

def load_policies_from_config(config: str) -> List[Policy]:
    policies = []
    config_data = json.loads(config)
    for policy_data in config_data["policies"]:
        policy = Policy(policy_data["name"], policy_data["rules"])
        policies.append(policy)
    return policies
