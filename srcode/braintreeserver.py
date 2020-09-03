import braintree, os
from config import Config

client_token = Config.gateway.client_token.generate({
    "customer_id": "testing101"
})