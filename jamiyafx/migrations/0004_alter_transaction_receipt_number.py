# Generated by Django 4.0.1 on 2023-05-26 10:28

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0003_transaction_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='receipt_number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', editable=False, length=3, max_length=3, prefix='', unique=True),
        ),
    ]