from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField("Hisob nomi", max_length=255)
    balance = models.DecimalField("Summa", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    TYPE_CHOICES = (
        ("income", "Kirim"),
        ("expense", "Chiqim"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField("Tur nomi", max_length=255)
    type = models.CharField("Turi", max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.type})"
