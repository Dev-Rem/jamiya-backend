# Generated by Django 4.0.1 on 2022-02-07 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0019_remove_generalledger_previous_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='currency',
            field=models.CharField(choices=[('NAIRA', 'NAIRA'), ('DOLLAR', 'DOLLAR'), ('POUND', 'POUND'), ('EURO', 'EURO')], default='DOLLAR', max_length=30, verbose_name='Station'),
        ),
    ]
