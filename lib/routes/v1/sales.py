from http import HTTPStatus
from flask import request, jsonify

from braintree.exceptions import NotFoundError
from marshmallow.exceptions import ValidationError

from lib.models.sale import SaleSchema
from lib.braintree_manager import BraintreeManager


def v1sales_get(sale_id: str):
    try:
        sale = BraintreeManager.get_gateway().transaction.find(sale_id)

    except NotFoundError as err:
        print(err)
        return jsonify({"errors": str(err)}), HTTPStatus.NOT_FOUND

    return jsonify({"sale": {"amount": float(sale.amount), "created_at": sale.created_at.isoformat()}}), HTTPStatus.OK


def v1sales_post():
    data = request.json

    # validate
    try:
        sale_data = SaleSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), HTTPStatus.BAD_REQUEST

    # push transaction
    sale = BraintreeManager.get_gateway().transaction.sale(sale_data)

    if sale.is_success:
        return jsonify({"sale_id": sale.transaction.id}), HTTPStatus.CREATED

    else:
        return jsonify({"errors": [err.message for err in sale.errors.deep_errors]}), HTTPStatus.BAD_REQUEST
