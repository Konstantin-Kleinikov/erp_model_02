from django.urls import path

from . import views


app_name = 'common'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index' ),
    path('currency/', views.CurrencyListView.as_view(), name='currency'),
]