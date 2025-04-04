"""Module for views of application common."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .mixins import CurrencyMixin
from .models import Currency


class IndexView(TemplateView):
    """Home page of erp application."""
    template_name = 'common/index.html'

class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('filter_by_name')
        if query:
            queryset = queryset.filter(name__icontains=query)
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
