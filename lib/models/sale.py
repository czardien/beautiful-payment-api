from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError


def _validate_amount(amount):
    try:
        float(amount)
    except ValueError:
        raise ValidationError(f"Not a float: {amount}.")


class SaleSchema(Schema):
    amount = fields.String(validate=_validate_amount)
    payment_method_nonce = fields.String()
