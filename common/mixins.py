"""Mixins for common application."""
from django.http import Http404

from common.forms import CurrencyForm, CurrencyRateForm
from common.models import Currency, CurrencyRate


class CurrencyMixin:
    model = Currency
    form_class = CurrencyForm
    pk_url_kwarg = 'currency_code'


class CurrencyRateMixin:
    model = CurrencyRate
    form_class = CurrencyRateForm


class CurrencyRateDetailMixin:
    def get_object(self, queryset=None):
        currency_code = self.kwargs.get('currency_code')
        rate_date = self.kwargs.get('date_str')
        try:
            return CurrencyRate.objects.get(
                currency__code=currency_code,
                rate_date=rate_date
            )
        except CurrencyRate.DoesNotExist:
            raise Http404(f"CurrencyRate with currency '{currency_code}' "
                          f"and date '{rate_date}' does not exist."
                          )
