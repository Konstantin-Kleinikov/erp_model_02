"""Module with forms for common application."""
from django import forms

from common.models import Currency, CurrencyRate


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = [
            'code',
            'name',
            'iso_code',
            'numeric_code',
            'note',
            # 'created_at',
            # 'created_by',
            # 'modified_at',
            # 'modified_by',
        ]


class CurrencyRateForm(forms.ModelForm):
    class Meta:
        model = CurrencyRate
        fields = [
            'currency',
            'rate_date',
            'nominal',
            'rate',
        ]


class DownloadRatesForm(forms.Form):
    rate_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
