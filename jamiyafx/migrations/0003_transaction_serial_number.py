# Generated by Django 4.0.1 on 2023-05-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0002_alter_transaction_receipt_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='serial_number',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True, unique=True),
        ),
    ]
