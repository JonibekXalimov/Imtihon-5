from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="amount",
            field=models.DecimalField("Summa", decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="transaction_type",
            field=models.CharField(
                choices=[("income", "Kirim"), ("expense", "Chiqim")],
                max_length=10,
            ),
        ),
    ]
