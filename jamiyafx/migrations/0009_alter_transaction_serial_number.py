# Generated by Django 4.0.1 on 2023-05-28 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0008_alter_currency_ngn_alter_transaction_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='serial_number',
            field=models.CharField(blank=True, default=0, max_length=1024, null=True, unique=True),
        ),
    ]