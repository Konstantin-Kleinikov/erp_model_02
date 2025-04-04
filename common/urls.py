from django.urls import path

from . import views

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
]