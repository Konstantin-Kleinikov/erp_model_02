"""Module with forms for common application."""
from django import forms

from common.models import Currency


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
