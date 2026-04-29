from django.conf import settings
from django.db import migrations, models


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


def normalize_defaults(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    Category = apps.get_model("finance", "Category")
    Wallet = apps.get_model("finance", "Wallet")

    for user in User.objects.all():
        old_to_new_categories = (
            ("Biznes daromadi", "Avans", "income"),
            ("Freelance", "Kunlik ish haqi", "income"),
            ("Transport", "Yo'lkira", "expense"),
            ("Oziq-ovqat", "Tushlik", "expense"),
            ("Sog'liq", "Salomatlik", "expense"),
        )

        for old_name, new_name, category_type in old_to_new_categories:
            old_qs = Category.objects.filter(
                user=user,
                name=old_name,
                type=category_type,
            )
            target_exists = Category.objects.filter(
                user=user,
                name=new_name,
                type=category_type,
            ).exists()
            if old_qs.exists() and not target_exists:
                old_qs.update(name=new_name)

        old_to_new_wallets = (
            ("Humo", "Karta"),
            ("Uzcard", "Valyuta"),
        )

        for old_name, new_name in old_to_new_wallets:
            old_wallet = Wallet.objects.filter(user=user, name=old_name).first()
            target_exists = Wallet.objects.filter(user=user, name=new_name).exists()
            if old_wallet and not target_exists:
                old_wallet.name = new_name
                old_wallet.save(update_fields=["name"])

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
        ("finance", "0002_seed_default_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField("Tur nomi", max_length=255),
        ),
        migrations.AlterField(
            model_name="category",
            name="type",
            field=models.CharField(
                "Turi",
                choices=[("income", "Kirim"), ("expense", "Chiqim")],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField("Hisob nomi", max_length=255),
        ),
        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(
                "Summa",
                decimal_places=2,
                default=0,
                max_digits=12,
            ),
        ),
        migrations.RunPython(normalize_defaults, migrations.RunPython.noop),
    ]
