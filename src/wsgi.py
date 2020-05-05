from flask import Flask, redirect, url_for

from lib.config import Config
from lib.routes import service
from lib.swagger import get_blueprint
from lib.braintree_manager import BraintreeManager

from lib.routes.v1.tokens import v1tokens
from lib.routes.v1.sales import v1sales_post, v1sales_get


application = Flask(Config.APP_NAME)
application.config.from_object(Config)

application.add_url_rule("/status", view_func=service.status, methods=["GET"])
application.add_url_rule("/metrics", view_func=service.metrics, methods=["GET"])

application.add_url_rule("/", view_func=lambda: redirect(url_for("status")), methods=["GET"])

application.add_url_rule("/v1/tokens", view_func=v1tokens, methods=["GET"], strict_slashes=False)
application.add_url_rule("/v1/sales", view_func=v1sales_post, methods=["POST"])
application.add_url_rule("/v1/sales/<sale_id>", view_func=v1sales_get, methods=["GET"])

blueprint = get_blueprint(Config.SWAGGER_URL, Config.SWAGGER_PATH, Config.APP_NAME)
application.register_blueprint(blueprint, url_prefix=Config.SWAGGER_URL)

BraintreeManager.from_config(Config.BRAINTREE_MERCHANT_ID, Config.BRAINTREE_PUBLIC_KEY, Config.BRAINTREE_PRIVATE_KEY)
