from django.conf import settings
from django.db import migrations


DEFAULT_CATEGORIES = [
    ("Oylik", "income"),
    ("Avans", "income"),
    ("Kunlik ish haqi", "income"),
    ("Yo'lkira", "expense"),
    ("Tushlik", "expense"),
    ("Salomatlik", "expense"),
]

DEFAULT_WALLETS = [
    ("Naqd pul", 0),
    ("Karta", 0),
    ("Valyuta", 0),
]


def seed_categories(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    Category = apps.get_model("finance", "Category")
    Wallet = apps.get_model("finance", "Wallet")

    for user in User.objects.all():
        for name, category_type in DEFAULT_CATEGORIES:
            Category.objects.get_or_create(
                user=user,
                name=name,
                type=category_type,
            )
        for name, balance in DEFAULT_WALLETS:
            Wallet.objects.get_or_create(
                user=user,
                name=name,
                defaults={"balance": balance},
            )


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
