from django import forms

from finance.models import Category, Wallet

from .models import Transaction


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["wallet", "category", "amount"]
        labels = {
            "category": "Kirim turi",
            "amount": "Summa",
        }
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["wallet"].queryset = Wallet.objects.filter(user=user)
        self.fields["category"].queryset = Category.objects.filter(
            user=user,
            type="income",
        )


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["wallet", "category", "amount"]
        labels = {
            "category": "Chiqim turi",
            "amount": "Summa",
        }
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["wallet"].queryset = Wallet.objects.filter(user=user)
        self.fields["category"].queryset = Category.objects.filter(
            user=user,
            type="expense",
        )
