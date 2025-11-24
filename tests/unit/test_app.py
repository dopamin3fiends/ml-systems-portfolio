import pytest
from src.backend.app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the ML Systems Portfolio' in response.data

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_non_existent_route(client):
    response = client.get('/non-existent')
    assert response.status_code == 404