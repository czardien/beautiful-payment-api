import pytest
from http import HTTPStatus

from src.wsgi import application


@pytest.fixture
def client():
    application.config['TESTING'] = True
    return application.test_client()


# GET /status
def test_status_returns_200(client):
    response = client.get("/status")
    assert response.status_code == HTTPStatus.OK
