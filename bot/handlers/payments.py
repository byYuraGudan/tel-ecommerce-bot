from eccomerceBot.settings import PAYPAL


class PaymentPayPal:

    def __init__(self, payload, provider_token, currency, start_parameter):
        self.payload = payload
        self.provider_token = provider_token
        self.currency = currency
        self.start_parameter = start_parameter

    @property
    def invoice_payment(self):
        return {
            'payload': self.payload,
            'provider_token': self.provider_token,
            'currency': self.currency,
            'start_parameter': self.start_parameter
        }


paypal = PaymentPayPal(**PAYPAL)
