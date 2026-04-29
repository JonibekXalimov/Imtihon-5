from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from finance.models import Wallet
from transactions.models import Transaction

from .i18n import TEXT, get_language


def total_amount(queryset):
    return queryset.aggregate(total=Sum("amount"))["total"] or 0


def build_report_rows(user, language="uz"):
    text = TEXT.get(language, TEXT["uz"])
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    base = Transaction.objects.filter(user=user)
    periods = (
        (text["daily"], base.filter(created_at__date=today)),
        (text["weekly"], base.filter(created_at__date__gte=week_start)),
        (text["monthly"], base.filter(created_at__date__gte=month_start)),
    )

    rows = []
    for label, queryset in periods:
        income = total_amount(queryset.filter(transaction_type="income"))
        expense = total_amount(queryset.filter(transaction_type="expense"))
        rows.append({
            "label": label,
            "income": income,
            "expense": expense,
            "net": income - expense,
        })

    return rows


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        total_income = total_amount(
            Transaction.objects.filter(user=user, transaction_type="income")
        )
        total_expense = total_amount(
            Transaction.objects.filter(user=user, transaction_type="expense")
        )

        total_wallet = Wallet.objects.filter(user=user).aggregate(
            total=Sum("balance")
        )["total"] or 0

        wallets = Wallet.objects.filter(user=user).order_by("name")
        last_transactions = Transaction.objects.filter(
            user=user,
            transaction_type__in=("income", "expense"),
        ).order_by("-created_at")[:10]

        context.update({
            "total_income": total_income,
            "total_expense": total_expense,
            "total_wallet": total_wallet,
            "wallets": wallets,
            "last_transactions": last_transactions,
        })

        return context


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "core/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_rows"] = build_report_rows(
            self.request.user,
            get_language(self.request),
        )
        return context


def set_language_view(request, language):
    if language in TEXT:
        request.session["app_language"] = language

    return redirect(request.GET.get("next") or "home")
