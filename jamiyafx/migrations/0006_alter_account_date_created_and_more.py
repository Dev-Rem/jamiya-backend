# Generated by Django 4.0.1 on 2022-02-03 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0005_alter_closingbalance_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='closingbalance',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='moneyin',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='moneyout',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='openingbalance',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Added'),
        ),
    ]
