import datetime

import pytest
from unittest.mock import MagicMock
from http import HTTPStatus
from braintree.exceptions import NotFoundError

from lib.braintree_manager import BraintreeManager
from src.wsgi import application


@pytest.fixture
def client():
    application.config['TESTING'] = True
    return application.test_client()


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


# POST /v1/sales/
def test_v1_sales_post_correct_data_returns_id_and_201(client, gateway):
    sale_mock = MagicMock()
    sale_mock.is_success = True
    sale_mock.transaction.id = "mock_sale_id"
    gateway.transaction.sale.return_value = sale_mock

    sales_body = {"amount": "100.0", "payment_method_nonce": "fake-valid-nonce"}
    response = client.post("/v1/sales", json=sales_body, follow_redirects=False)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json["sale_id"] == "mock_sale_id"


def test_v1_sales_post_invalid_amount_returns_error_and_400(client, gateway):
    wrong_sales_body = {"amount": "not-a-float", "payment_method_nonce": "fake-valid-nonce"}
    response = client.post("/v1/sales", json=wrong_sales_body, follow_redirects=False)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["errors"] == {"amount": ["Not a float: not-a-float."]}


def test_v1_sales_post_invalid_data_returns_error_and_400(client, gateway):
    err_mock = MagicMock()
    err_mock.message = "mock error message"

    sale_mock = MagicMock()
    sale_mock.is_success = False
    sale_mock.errors.deep_errors = [err_mock]
    gateway.transaction.sale.return_value = sale_mock

    wrong_sales_body = {"amount": "100.0", "payment_method_nonce": "wrong"}
    response = client.post("/v1/sales", json=wrong_sales_body, follow_redirects=False)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["errors"] == ["mock error message"]


# GET /v1/sales/{sale_id}
def test_v1_sales_get_existing_sale_id_returns_correct_id_and_200(client, gateway):
    sale_mock = MagicMock()
    sale_mock.amount = "10.0"
    sale_mock.created_at = datetime.datetime(2020, 1, 1)
    gateway.transaction.find.return_value = sale_mock

    response = client.get(f"v1/sales/fake_id", follow_redirects=False)

    assert response.status_code == HTTPStatus.OK
    assert response.json["sale"]["amount"] == 10.0
    assert response.json["sale"]["created_at"] == "2020-01-01T00:00:00"


def test_v1_sales_get_non_existing_sale_id_returns_404(client, gateway):
    gateway.transaction.find = MagicMock(side_effect=NotFoundError("mock not found error"))

    response = client.get(f"v1/sales/fake_id", follow_redirects=False)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json["errors"] == "mock not found error"
