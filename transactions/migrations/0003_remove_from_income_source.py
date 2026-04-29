from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0003_category_labels_and_names"),
        ("transactions", "0002_remove_transfer_choice"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="from_income_source",
        ),
    ]
