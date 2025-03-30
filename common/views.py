"""Module for views of application common."""
from django.views.generic import ListView, TemplateView

from .models import Currency


class IndexView(TemplateView):
    """Home page of erp application."""
    template_name = 'common/index.html'

class CurrencyListView(ListView):
    model = Currency
    paginate_by = 4
    #template_name = 'common/currency_list.html'

