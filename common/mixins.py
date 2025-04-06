"""Mixins for common application."""
from common.forms import CurrencyForm, CurrencyRateForm
from common.models import Currency, CurrencyRate


class CurrencyMixin:
    model = Currency
    form_class = CurrencyForm
    pk_url_kwarg = 'currency_code'


class CurrencyRateMixin:
    model = CurrencyRate
    form_class = CurrencyRateForm

