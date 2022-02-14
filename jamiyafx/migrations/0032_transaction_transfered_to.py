# Generated by Django 4.0.1 on 2022-02-14 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0031_rename_given_mode_transaction_give_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transfered_to',
            field=models.CharField(choices=[('ZENITH BANK', 'ZENITH BANK'), ('PROVIDUS BANK', 'PROVIDUS BANK')], default='ZENITH BANK', max_length=50, verbose_name='Transfered To'),
        ),
    ]
