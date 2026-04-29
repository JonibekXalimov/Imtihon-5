from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from finance.models import Category

from .forms import ExpenseForm, IncomeForm
from .models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions/list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        qs = Transaction.objects.filter(
            user=self.request.user,
            transaction_type__in=("income", "expense"),
        )

        t_type = self.request.GET.get("type")
        date = self.request.GET.get("date")
        min_amount = self.request.GET.get("min_amount")
        max_amount = self.request.GET.get("max_amount")
        category_id = self.request.GET.get("category")

        if t_type in ("income", "expense"):
            qs = qs.filter(transaction_type=t_type)

        if date:
            qs = qs.filter(created_at__date=date)

        if min_amount:
            qs = qs.filter(amount__gte=min_amount)

        if max_amount:
            qs = qs.filter(amount__lte=max_amount)

        if category_id:
            qs = qs.filter(category_id=category_id)

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            user=self.request.user,
            type__in=("income", "expense"),
        ).order_by("type", "name")
        return context


class AddIncomeView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = IncomeForm
    template_name = "transactions/add_income.html"
    success_url = reverse_lazy("transactions:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        wallet = form.instance.wallet
        wallet.balance += form.cleaned_data["amount"]
        wallet.save()

        form.instance.user = self.request.user
        form.instance.transaction_type = "income"

        messages.success(self.request, "Kirim saqlandi")
        return super().form_valid(form)


class SpendView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = ExpenseForm
    template_name = "transactions/spend.html"
    success_url = reverse_lazy("transactions:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        wallet = form.instance.wallet
        wallet.balance -= form.cleaned_data["amount"]
        wallet.save()

        form.instance.user = self.request.user
        form.instance.transaction_type = "expense"

        messages.success(self.request, "Chiqim saqlandi")
        return super().form_valid(form)
