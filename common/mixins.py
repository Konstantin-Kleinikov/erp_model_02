"""Mixins for common application."""
from common.forms import CurrencyForm
from common.models import Currency


class CurrencyMixin:
    model = Currency
    form_class = CurrencyForm
    pk_url_kwarg = 'currency_code'
