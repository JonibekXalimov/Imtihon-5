from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Category, Wallet


class WalletListView(LoginRequiredMixin, ListView):
    model = Wallet
    template_name = "finance/wallet/list.html"
    context_object_name = "wallets"

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user).order_by("name")


class WalletCreateView(LoginRequiredMixin, CreateView):
    model = Wallet
    fields = ["name", "balance"]
    template_name = "finance/wallet/form.html"
    success_url = reverse_lazy("wallet-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WalletUpdateView(LoginRequiredMixin, UpdateView):
    model = Wallet
    fields = ["name"]
    template_name = "finance/wallet/form.html"
    success_url = reverse_lazy("wallet-list")

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)


class WalletDeleteView(LoginRequiredMixin, DeleteView):
    model = Wallet
    template_name = "finance/confirm_delete.html"
    success_url = reverse_lazy("wallet-list")

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "finance/category/list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by("type", "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.get_queryset()
        context["income_categories"] = categories.filter(type="income")
        context["expense_categories"] = categories.filter(type="expense")
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name", "type"]
    template_name = "finance/category/form.html"
    success_url = reverse_lazy("category-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
