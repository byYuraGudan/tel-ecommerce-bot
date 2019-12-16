from eccomerceBot.settings import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
DJANGO_TELEGRAMBOT = {

    'MODE': 'POLLING',
    'BOTS': [
        {
           'TOKEN': '821409346:AAE1rlVNdtJRwZxh7JpiO-ZDefOmW0uSKIY',
        },
    ],
}

PAYPAL = {
    'provider_token': '635983722:LIVE:i86036110941',
    'currency': 'UAH',
    'payload': 'payload-books',
    'start_parameter': 'payment-books'
}