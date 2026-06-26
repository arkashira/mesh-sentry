from mesh_sentry import MeshSentry, Node, Connection

def test_add_node():
    mesh_sentry = MeshSentry()
    mesh_sentry.add_node("node1", 0.1, 10.0)
    assert mesh_sentry.nodes["node1"].name == "node1"
    assert mesh_sentry.nodes["node1"].error_rate == 0.1
    assert mesh_sentry.nodes["node1"].latency == 10.0

def test_add_connection():
    mesh_sentry = MeshSentry()
    mesh_sentry.add_node("node1", 0.1, 10.0)
    mesh_sentry.add_node("node2", 0.2, 20.0)
    mesh_sentry.add_connection("node1", "node2", 50)
    assert mesh_sentry.connections["node1-node2"].source == "node1"
    assert mesh_sentry.connections["node1-node2"].target == "node2"
    assert mesh_sentry.connections["node1-node2"].traffic == 50

def test_get_topology():
    mesh_sentry = MeshSentry()
    mesh_sentry.add_node("node1", 0.1, 10.0)
    mesh_sentry.add_node("node2", 0.2, 20.0)
    mesh_sentry.add_connection("node1", "node2", 50)
    topology = mesh_sentry.get_topology()
    assert len(topology["nodes"]) == 2
    assert len(topology["connections"]) == 1

def test_update_traffic():
    mesh_sentry = MeshSentry()
    mesh_sentry.add_node("node1", 0.1, 10.0)
    mesh_sentry.add_node("node2", 0.2, 20.0)
    mesh_sentry.add_connection("node1", "node2", 50)
    mesh_sentry.update_traffic()
    assert mesh_sentry.connections["node1-node2"].traffic != 50

def test_get_traffic_flow():
    mesh_sentry = MeshSentry()
    mesh_sentry.add_node("node1", 0.1, 10.0)
    mesh_sentry.add_node("node2", 0.2, 20.0)
    mesh_sentry.add_connection("node1", "node2", 50)
    traffic_flow = mesh_sentry.get_traffic_flow()
    assert traffic_flow["node1-node2"] == 50

def test_get_error_rates():
    mesh_sentry = MeshSentry()
    mesh_sentry.add_node("node1", 0.1, 10.0)
    mesh_sentry.add_node("node2", 0.2, 20.0)
    error_rates = mesh_sentry.get_error_rates()
    assert error_rates["node1"] == 0.1
    assert error_rates["node2"] == 0.2

def test_get_latency():
    mesh_sentry = MeshSentry()
    mesh_sentry.add_node("node1", 0.1, 10.0)
    mesh_sentry.add_node("node2", 0.2, 20.0)
    latency = mesh_sentry.get_latency()
    assert latency["node1"] == 10.0
    assert latency["node2"] == 20.0
