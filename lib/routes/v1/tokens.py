from http import HTTPStatus
from flask import jsonify

from lib.braintree_manager import BraintreeManager


def v1tokens():
    # the token is to be used on the client-side integration when requestion a payment nonce
    token = BraintreeManager.get_gateway().client_token.generate()
    return jsonify({"token": token}), HTTPStatus.OK
