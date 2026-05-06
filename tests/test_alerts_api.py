from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HTTP_OK = 200


def test_get_alerts_empty():
    """Test GET /alerts returns empty list initially."""
    response = client.get("/alerts")
    assert response.status_code == HTTP_OK
    assert response.json() == []


def test_get_alerts_with_data():
    """Test GET /alerts returns alerts list."""
    response = client.get("/alerts")
    assert response.status_code == HTTP_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_alerts_by_region():
    """Test GET /alerts/{region} returns alerts for specific region."""
    response = client.get("/alerts/Jaboatão dos Guararapes")
    assert response.status_code == HTTP_OK
    assert isinstance(response.json(), list)


def test_get_regions_empty():
    """Test GET /regions returns empty list initially."""
    response = client.get("/regions")
    assert response.status_code == HTTP_OK
    assert response.json() == []


def test_get_regions_with_data():
    """Test GET /regions returns regions list."""
    response = client.get("/regions")
    assert response.status_code == HTTP_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_health():
    """Test GET /health returns ok status."""
    response = client.get("/health")
    assert response.status_code == HTTP_OK
    assert response.json() == {"status": "ok"}
