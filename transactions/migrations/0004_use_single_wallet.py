import django.db.models.deletion
from django.db import migrations, models


def move_wallet_data(apps, schema_editor):
    Transaction = apps.get_model("transactions", "Transaction")

    for transaction in Transaction.objects.all():
        transaction.wallet = transaction.to_wallet or transaction.from_wallet
        transaction.save(update_fields=["wallet"])


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0004_delete_income_source"),
        ("transactions", "0003_remove_from_income_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="wallet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="transactions",
                to="finance.wallet",
                verbose_name="Hisob",
            ),
        ),
        migrations.RunPython(move_wallet_data, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="transaction",
            name="from_wallet",
        ),
        migrations.RemoveField(
            model_name="transaction",
            name="to_wallet",
        ),
    ]
