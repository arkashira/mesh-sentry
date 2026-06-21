from mesh_sentry import authenticate_with_istio, ingest_telemetry_data, get_connection_status, MeshMateConnection, IstioCredentials

def test_authenticate_with_istio_valid_credentials():
    credentials = IstioCredentials("admin", "password")
    connection = MeshMateConnection("https://istio.example.com", credentials)
    assert authenticate_with_istio(connection) == True

def test_authenticate_with_istio_invalid_credentials():
    credentials = IstioCredentials("wrong", "credentials")
    connection = MeshMateConnection("https://istio.example.com", credentials)
    assert authenticate_with_istio(connection) == False

def test_ingest_telemetry_data_valid_credentials():
    credentials = IstioCredentials("admin", "password")
    connection = MeshMateConnection("https://istio.example.com", credentials)
    assert ingest_telemetry_data(connection) == {"traffic_flows": [], "performance_metrics": {}}

def test_ingest_telemetry_data_invalid_credentials():
    credentials = IstioCredentials("wrong", "credentials")
    connection = MeshMateConnection("https://istio.example.com", credentials)
    try:
        ingest_telemetry_data(connection)
        assert False
    except Exception as e:
        assert str(e) == "Authentication failed"

def test_get_connection_status_valid_credentials():
    credentials = IstioCredentials("admin", "password")
    connection = MeshMateConnection("https://istio.example.com", credentials)
    assert get_connection_status(connection) == "Connected"

def test_get_connection_status_invalid_credentials():
    credentials = IstioCredentials("wrong", "credentials")
    connection = MeshMateConnection("https://istio.example.com", credentials)
    assert get_connection_status(connection) == "Connection failed: Authentication failed"
