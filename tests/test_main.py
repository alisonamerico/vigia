from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


HTTP_OK = 200


def test_health_check():
    """Test /health endpoint returns ok status."""
    response = client.get('/health')
    assert response.status_code == HTTP_OK
    assert response.json() == {'status': 'ok'}
