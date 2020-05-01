import braintree


class BraintreeManager:
    merchant_id: str
    public_key: str
    private_key: str

    @classmethod
    def from_config(cls, merchant_id: str, public_key: str, private_key: str):
        cls.merchant_id = merchant_id
        cls.public_key = public_key
        cls.private_key = private_key

    @classmethod
    def get_gateway(cls):
        return braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=cls.merchant_id,
                public_key=cls.public_key,
                private_key=cls.private_key
            )
        )
