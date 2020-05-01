import os


class Config:
    APP_NAME = os.environ.get("APP_NAME", "Beautiful Payment API")
    TESTING = True
    DEBUG = True

    BRAINTREE_MERCHANT_ID = os.environ["BRAINTREE_MERCHANT_ID"]
    BRAINTREE_PUBLIC_KEY = os.environ["BRAINTREE_PUBLIC_KEY"]
    BRAINTREE_PRIVATE_KEY = os.environ["BRAINTREE_PRIVATE_KEY"]

    SWAGGER_URL = "/docs"
    SWAGGER_PATH = "swagger.yaml"
