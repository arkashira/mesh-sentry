import pytest
from mesh_sentry import MeshSentry, Service

def test_add_service():
    mesh_sentry = MeshSentry()
    service = Service("test-service", {"requests": 10.0, "response_time": 100.0})
    mesh_sentry.add_service(service)
    assert service.name in mesh_sentry.services

def test_get_service_topology():
    mesh_sentry = MeshSentry()
    service1 = Service("test-service1", {"requests": 10.0, "response_time": 100.0})
    service2 = Service("test-service2", {"requests": 20.0, "response_time": 200.0})
    mesh_sentry.add_service(service1)
    mesh_sentry.add_service(service2)
    topology = mesh_sentry.get_service_topology()
    assert "test-service1" in topology
    assert "test-service2" in topology
    assert len(topology["test-service1"]) == 2
    assert len(topology["test-service2"]) == 2

def test_update_service_performance_metrics():
    mesh_sentry = MeshSentry()
    service = Service("test-service", {"requests": 10.0, "response_time": 100.0})
    mesh_sentry.add_service(service)
    new_metrics = {"requests": 20.0, "response_time": 200.0}
    mesh_sentry.update_service_performance_metrics("test-service", new_metrics)
    assert mesh_sentry.get_service_performance_metrics("test-service") == new_metrics

def test_get_service_performance_metrics():
    mesh_sentry = MeshSentry()
    service = Service("test-service", {"requests": 10.0, "response_time": 100.0})
    mesh_sentry.add_service(service)
    metrics = mesh_sentry.get_service_performance_metrics("test-service")
    assert metrics == {"requests": 10.0, "response_time": 100.0}

def test_get_service_performance_metrics_service_not_found():
    mesh_sentry = MeshSentry()
    with pytest.raises(ValueError):
        mesh_sentry.get_service_performance_metrics("non-existent-service")
