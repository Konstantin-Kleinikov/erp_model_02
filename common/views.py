"""Module for views of application common."""
import logging
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from http import HTTPStatus

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .constants import PAGINATOR_VALUE
from .forms import DownloadRatesForm
from .mixins import CurrencyMixin, CurrencyRateMixin
from .models import Currency, CurrencyRate

# TODO Not working
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - '
           '%(filename)s->%(funcName)s:%(lineno)d, - %(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


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


class CurrencyRateCreateView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    CreateView
):
    pk_url_kwarg = 'rate_date'

    def get_initial(self):
        initial = super().get_initial()
        initial['rate_date'] = timezone.now().date()
        return initial


class CurrencyRateDetailView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    DetailView
):
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


class CurrencyRateEditView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    UpdateView
):
    pass


class CurrencyRateDeleteView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    DeleteView
):
    pass


def get_currency_rates(request):
    date_str = request.GET.get(
        'rate_date',
        timezone.now().date().strftime('%Y-%m-%d')
    )
    # Convert date string to dd/mm/yyyy format
    date_req = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req}'

    logging.debug(f'Sending GET request to {url}')
    response = requests.get(url)
    logging.debug(
        f'Response from GET request to {url}: '
        f'{response.status_code}, {response.text}'
    )

    if response.status_code == HTTPStatus.OK:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        # Fetch all currencies and existing rates in one query
        rate_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        existing_rates = set(
            CurrencyRate.objects.filter(rate_date=rate_date)
            .values_list('currency__code', flat=True)
        )
        currencies = {
            currency.code: currency
            for currency in Currency.objects.all()
        }

        rates = []
        for currency in root.findall('Valute'):
            code = currency.find('CharCode').text
            value = float(currency.find('Value').text.replace(',', '.'))
            nominal = int(currency.find('Nominal').text)

            # Check if the currency exists and rate is not already added
            if code in currencies and code not in existing_rates:
                CurrencyRate.objects.create(
                    currency=currencies[code],
                    rate_date=rate_date,
                    nominal=nominal,
                    rate=value,
                    created_by=request.user.username,
                )
                rates.append({'code': code, 'value': value, 'nominal': nominal})

        return render(
            request,
            'common/download_rates.html',
            {
                'form': DownloadRatesForm(initial={'rate_date': date_str}),
                'rates': rates
            }
        )
    else:
        logging.error(f'Failed to fetch data from {url}')
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
