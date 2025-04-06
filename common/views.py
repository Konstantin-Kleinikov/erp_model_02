"""Module for views of application common."""
import xml.etree.ElementTree as ET
from datetime import datetime
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
import requests

from .constants import PAGINATOR_VALUE
from .forms import DownloadRatesForm
from .mixins import CurrencyMixin, CurrencyRateMixin
from .models import Currency, CurrencyRate


class IndexView(TemplateView):
    """Home page of erp application."""

    template_name = 'common/index.html'


class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    paginate_by = PAGINATOR_VALUE

    def get_queryset(self):
        queryset = super().get_queryset()
        text_of_filter = self.request.GET.get('filter_by_name')
        if text_of_filter:
            queryset = queryset.filter(name__icontains=text_of_filter)
        return queryset


class CurrencyDetailView(LoginRequiredMixin, CurrencyMixin, DetailView):
    model = Currency


class CurrencyCreateView(LoginRequiredMixin, CurrencyMixin, CreateView):
    model = Currency

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        return super().form_valid(form)


class CurrencyUpdateView(LoginRequiredMixin, CurrencyMixin, UpdateView):
    model = Currency

    def form_valid(self, form):
        form.instance.modified_by = self.request.user.username
        return super().form_valid(form)


class CurrencyDeleteView(LoginRequiredMixin, CurrencyMixin, DeleteView):
    model = Currency
    success_url = reverse_lazy('common:currency_list')


class CurrencyRateAllListView(LoginRequiredMixin, ListView):
    model = CurrencyRate
    paginate_by = PAGINATOR_VALUE


class CurrencyRateDateListView(LoginRequiredMixin, ListView):
    model = CurrencyRate
    paginate_by = PAGINATOR_VALUE


class CurrencyRateListView(LoginRequiredMixin, ListView):
    model = CurrencyRate
    paginate_by = PAGINATOR_VALUE


class CurrencyRateCreateView(LoginRequiredMixin, CurrencyRateMixin, CreateView):
    pk_url_kwarg = 'rate_date'

    def get_initial(self):
        initial = super().get_initial()
        initial['rate_date'] = timezone.now().date()
        return initial


def get_currency_rates(request):
    date_str = request.GET.get('rate_date', timezone.now().date().strftime('%Y-%m-%d'))
    # Преобразуем строку даты в формат dd/mm/yyyy
    date_req = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req}'

    response = requests.get(url)
    if response.status_code == HTTPStatus.OK:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        rates = []
        for currency in root.findall('Valute'):
            code = currency.find('CharCode').text
            value = float(currency.find('Value').text.replace(',', '.'))
            nominal = int(currency.find('Nominal').text)

            # Check if the Currency instance exists
            try:
                currency_instance = Currency.objects.get(code=code)
                rate_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                # Check if the CurrencyRate instance already exists
                if not (CurrencyRate.objects.filter(
                        currency=currency_instance,
                        rate_date=rate_date
                )
                        .exists()):
                    # Create and save the new CurrencyRate instance
                    CurrencyRate.objects.create(
                        currency=currency_instance,
                        rate_date=rate_date,
                        nominal=nominal,
                        rate=value,
                        created_by=request.user.username,
                    )
                    rates.append({'code': code, 'value': value, 'nominal': nominal})
            except Currency.DoesNotExist:
                # Skip if the currency does not exist
                continue

        # return render(request, 'common/currencyrate_list.html', {'date': date_str, 'rates': rates})
        return HttpResponseRedirect(
            reverse('common:currency_rates_currency',
                    )
        )
    else:
        return HttpResponse(
            'Error fetching data from the Bank of Russia',
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )

def download_rates(request):
    initial_data = {'rate_date': timezone.now().date()}
    form = DownloadRatesForm(initial=initial_data)
    return render(
        request,
        'common/download_rates.html',
        {'form': form}
    )