from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0003_category_labels_and_names"),
        ("transactions", "0003_remove_from_income_source"),
    ]

    operations = [
        migrations.DeleteModel(
            name="IncomeSource",
        ),
    ]
