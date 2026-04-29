from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Transaction(models.Model):
    TYPE_CHOICES = (
        ("income", "Kirim"),
        ("expense", "Chiqim"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField("Summa", max_digits=12, decimal_places=2)

    wallet = models.ForeignKey(
        "finance.Wallet",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
        verbose_name="Hisob",
    )

    category = models.ForeignKey(
        "finance.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
