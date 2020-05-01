import os
import logging
from http import HTTPStatus
from flask import jsonify

from lib.braintree_manager import BraintreeManager


def v1tokens():
    # the token is to be used on the client-side integration when requestion a payment nonce
    logging.error(os.environ)
    logging.error(os.environ.get("BRAINTREE_MERCHANT_ID"))
    logging.error(os.environ.get("BRAINTREE_PUBLIC_KEY"))
    logging.error(os.environ.get("BRAINTREE_PRIVATE_KEY"))
    token = BraintreeManager.get_gateway().client_token.generate()
    return jsonify({"token": token}), HTTPStatus.OK
