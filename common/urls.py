from django.urls import path

from . import views
from .views import CurrencyRateCreateView, get_currency_rates, download_rates, CurrencyRateEditView, \
    CurrencyRateDetailView, CurrencyRateDeleteView

app_name = 'common'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index' ),
    path(
        'currency/',
        views.CurrencyListView.as_view(),
        name='currency_list'
    ),
    path(
        'currency/detail/<str:currency_code>/',
        views.CurrencyDetailView.as_view(),
        name='currency_detail'
    ),
    path(
        'currency/create/',
        views.CurrencyCreateView.as_view(),
        name='currency_create'
    ),
    path(
        'currency/edit/<str:currency_code>/',
        views.CurrencyUpdateView.as_view(),
        name='currency_edit'
    ),
    path(
        'currency/delete/<str:currency_code>/',
        views.CurrencyDeleteView.as_view(),
        name='currency_delete'
    ),
    path(
        'currency_rates/',
        views.CurrencyRateAllListView.as_view(),
        name='currency_rates'
    ),
    path(
        'currency_rates/<str:date_str>/',
        views.CurrencyRateDateListView.as_view(),
        name='currency_rates_date'
    ),
    path(
        'currency_rates/<str:currency_code>/',
        views.CurrencyRateListView.as_view(),
        name='currency_rates_currency'
    ),
    path(
        'currency_rates/',
        views.CurrencyRateListView.as_view(),
        name='currency_rates_currency'
    ),
    path(
        'currency_rates/create/<str:date_str>/',
        CurrencyRateCreateView.as_view(),
        name='currency_rates_create'
    ),
    path(
        'currency_rates/<str:currency_code>/<str:date_str>/',
        CurrencyRateDetailView.as_view(),
        name='currency_rates_detail'
    ),
    path(
        'currency_rates/edit/<str:currency_code>/<str:date_str>/',
        CurrencyRateEditView.as_view(),
        name='currency_rates_edit'
    ),
    path(
        'currency_rates/delete/<str:currency_code>/<str:date_str>/',
        CurrencyRateDeleteView.as_view(),
        name='currency_rates_delete'
    ),
    path(
        'get_currency_rates/',
        get_currency_rates,
        name='get_currency_rates'
    ),
    path(
        'download_rates/',
        download_rates,
        name='download_rates'
    ),
]