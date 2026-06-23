import pytest
from mesh_sentry import MeshSentry, Policy, Alert, load_policies_from_config

def test_add_policy():
    mesh_sentry = MeshSentry()
    policy = Policy("test_policy", ["rule1", "rule2"])
    mesh_sentry.add_policy(policy)
    assert len(mesh_sentry.policies) == 1

def test_enforce_policies():
    mesh_sentry = MeshSentry()
    policy = Policy("test_policy", ["rule1", "rule2"])
    mesh_sentry.add_policy(policy)
    service_communication = "This is a test communication with rule1"
    triggered_alerts = mesh_sentry.enforce_policies(service_communication)
    assert len(triggered_alerts) == 1
    assert triggered_alerts[0].policy_name == "test_policy"

def test_load_policies_from_config():
    config = '{"policies": [{"name": "policy1", "rules": ["rule1", "rule2"]}, {"name": "policy2", "rules": ["rule3", "rule4"]}]}'
    policies = load_policies_from_config(config)
    assert len(policies) == 2
    assert policies[0].name == "policy1"
    assert policies[1].name == "policy2"

def test_get_alerts():
    mesh_sentry = MeshSentry()
    alert = Alert("test_policy", "This is a test alert")
    mesh_sentry.add_alert(alert)
    alerts = mesh_sentry.get_alerts()
    assert len(alerts) == 1
    assert alerts[0].policy_name == "test_policy"

def test_enforce_policies_no_trigger():
    mesh_sentry = MeshSentry()
    policy = Policy("test_policy", ["rule1", "rule2"])
    mesh_sentry.add_policy(policy)
    service_communication = "This is a test communication with no rules"
    triggered_alerts = mesh_sentry.enforce_policies(service_communication)
    assert len(triggered_alerts) == 0
