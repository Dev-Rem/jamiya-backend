# Generated by Django 4.0.1 on 2022-02-17 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0035_generalledger_previous_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['-date_created']},
        ),
    ]