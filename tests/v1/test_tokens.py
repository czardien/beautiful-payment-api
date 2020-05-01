import pytest
from unittest.mock import MagicMock
from http import HTTPStatus

from src.wsgi import application
from lib.braintree_manager import BraintreeManager


@pytest.fixture(scope='function')
def gateway():
    braintree_gateway_mock = MagicMock()
    braintree_gateway_mock.client_token.generate.return_value = "generated_token"

    get_gateway_mock = MagicMock()
    get_gateway_mock.return_value = braintree_gateway_mock

    get_gateway_bak = BraintreeManager.get_gateway
    BraintreeManager.get_gateway = get_gateway_mock
    yield braintree_gateway_mock
    BraintreeManager.get_gateway = get_gateway_bak


@pytest.fixture
def client():
    application.config['TESTING'] = True
    return application.test_client()


# GET /v1/tokens
def test_v1_tokens_get_calls_gateway_and_return_token_and_200(client, gateway):
    response = client.get("v1/tokens")

    assert response.status_code == HTTPStatus.OK
    assert response.json.get("token", None) == "generated_token"
