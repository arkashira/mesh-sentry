from mesh_sentry import MeshSentry, Service

def test_add_service():
    mesh_sentry = MeshSentry()
    service = Service('test-service', 'test-namespace', 'healthy', 100)
    mesh_sentry.add_service(service)
    assert len(mesh_sentry.services) == 1

def test_filter_services_by_name():
    mesh_sentry = MeshSentry()
    service1 = Service('test-service1', 'test-namespace', 'healthy', 100)
    service2 = Service('test-service2', 'test-namespace', 'unhealthy', 50)
    mesh_sentry.add_service(service1)
    mesh_sentry.add_service(service2)
    filtered_services = mesh_sentry.filter_services(name='test-service1')
    assert len(filtered_services) == 1
    assert filtered_services[0].name == 'test-service1'

def test_filter_services_by_namespace():
    mesh_sentry = MeshSentry()
    service1 = Service('test-service1', 'test-namespace1', 'healthy', 100)
    service2 = Service('test-service2', 'test-namespace2', 'unhealthy', 50)
    mesh_sentry.add_service(service1)
    mesh_sentry.add_service(service2)
    filtered_services = mesh_sentry.filter_services(namespace='test-namespace1')
    assert len(filtered_services) == 1
    assert filtered_services[0].namespace == 'test-namespace1'

def test_get_service_health():
    mesh_sentry = MeshSentry()
    service = Service('test-service', 'test-namespace', 'healthy', 100)
    mesh_sentry.add_service(service)
    assert mesh_sentry.get_service_health('test-service') == 'healthy'

def test_get_service_traffic():
    mesh_sentry = MeshSentry()
    service = Service('test-service', 'test-namespace', 'healthy', 100)
    mesh_sentry.add_service(service)
    assert mesh_sentry.get_service_traffic('test-service') == 100

def test_visualize_mesh():
    mesh_sentry = MeshSentry()
    service1 = Service('test-service1', 'test-namespace1', 'healthy', 100)
    service2 = Service('test-service2', 'test-namespace2', 'unhealthy', 50)
    mesh_sentry.add_service(service1)
    mesh_sentry.add_service(service2)
    mesh_data = mesh_sentry.visualize_mesh()
    assert len(mesh_data) == 2
    assert mesh_data['test-service1']['namespace'] == 'test-namespace1'
    assert mesh_data['test-service1']['health'] == 'healthy'
    assert mesh_data['test-service1']['traffic'] == 100
