from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


@pytest.fixture
def client():
    """Create test client with overridden DB dependency."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    mock = AsyncMock()
    result = AsyncMock()
    result.scalars.return_value.all.return_value = []
    mock.execute.return_value = result
    return mock


def test_health_endpoint(client):
    """Test GET /health returns ok status."""
    response = client.get('/health')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ok'}


def test_health_trailing_slash(client):
    """Test GET /health/ also works."""
    response = client.get('/health/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ok'}


def test_get_alerts_default(client):
    """Test GET /alerts returns 200."""
    response = client.get('/alerts')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_alerts_with_mock_db(client, mock_db):
    """Test GET /alerts uses db session dependency."""
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get('/alerts')
    assert response.status_code == HTTPStatus.OK
    app.dependency_overrides.clear()


def test_get_alerts_by_region(client):
    """Test GET /alerts/{region} returns list."""
    response = client.get('/alerts/Recife')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


def test_get_regions(client):
    """Test GET /regions returns 200."""
    response = client.get('/regions')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_regions_with_mock_db(client, mock_db):
    """Test GET /regions uses db session dependency."""
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get('/regions')
    assert response.status_code == HTTPStatus.OK
    app.dependency_overrides.clear()


def test_get_nonexistent_route(client):
    """Test nonexistent route returns 404."""
    response = client.get('/nonexistent')
    assert response.status_code == HTTPStatus.NOT_FOUND
