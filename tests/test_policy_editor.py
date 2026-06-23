import pytest
from policy_editor import Policy, PolicyEditor, TrafficGraph

def test_get_policy_diff():
    current_policy = Policy([{"rule1": "value1"}, {"rule2": "value2"}])
    proposed_policy = Policy([{"rule1": "value1"}, {"rule3": "value3"}])
    policy_editor = PolicyEditor(current_policy, proposed_policy)
    diff = policy_editor.get_policy_diff()
    assert "Current Policy" in diff
    assert "Proposed Policy" in diff

def test_simulate_traffic_graph():
    current_policy = Policy([{"rule1": "value1"}, {"rule2": "value2"}])
    proposed_policy = Policy([{"rule1": "value1"}, {"rule3": "value3"}])
    policy_editor = PolicyEditor(current_policy, proposed_policy)
    traffic_graph = policy_editor.simulate_traffic_graph()
    assert isinstance(traffic_graph, TrafficGraph)
    assert traffic_graph.nodes == ["Node1", "Node2", "Node3"]
    assert traffic_graph.edges == [("Node1", "Node2"), ("Node2", "Node3")]

def test_confirm_rollout():
    current_policy = Policy([{"rule1": "value1"}, {"rule2": "value2"}])
    proposed_policy = Policy([{"rule1": "value1"}, {"rule3": "value3"}])
    policy_editor = PolicyEditor(current_policy, proposed_policy)
    result = policy_editor.confirm_rollout()
    assert result is True

def test_cancel_rollout():
    current_policy = Policy([{"rule1": "value1"}, {"rule2": "value2"}])
    proposed_policy = Policy([{"rule1": "value1"}, {"rule3": "value3"}])
    policy_editor = PolicyEditor(current_policy, proposed_policy)
    result = policy_editor.cancel_rollout()
    assert result is True

def test_policy_editor_init():
    current_policy = Policy([{"rule1": "value1"}, {"rule2": "value2"}])
    proposed_policy = Policy([{"rule1": "value1"}, {"rule3": "value3"}])
    policy_editor = PolicyEditor(current_policy, proposed_policy)
    assert policy_editor.current_policy == current_policy
    assert policy_editor.proposed_policy == proposed_policy
