# Generated by Django 4.0.1 on 2023-04-19 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jamiyafx', '0049_currency_remove_account_dollar_remove_account_euro_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='closingbalance',
            name='dollar',
        ),
        migrations.RemoveField(
            model_name='closingbalance',
            name='euro',
        ),
        migrations.RemoveField(
            model_name='closingbalance',
            name='naira',
        ),
        migrations.RemoveField(
            model_name='closingbalance',
            name='pound',
        ),
        migrations.RemoveField(
            model_name='customerledger',
            name='dollar',
        ),
        migrations.RemoveField(
            model_name='customerledger',
            name='euro',
        ),
        migrations.RemoveField(
            model_name='customerledger',
            name='naira',
        ),
        migrations.RemoveField(
            model_name='customerledger',
            name='pound',
        ),
        migrations.RemoveField(
            model_name='generalledger',
            name='dollar',
        ),
        migrations.RemoveField(
            model_name='generalledger',
            name='euro',
        ),
        migrations.RemoveField(
            model_name='generalledger',
            name='naira',
        ),
        migrations.RemoveField(
            model_name='generalledger',
            name='pound',
        ),
        migrations.RemoveField(
            model_name='moneyin',
            name='dollar',
        ),
        migrations.RemoveField(
            model_name='moneyin',
            name='euro',
        ),
        migrations.RemoveField(
            model_name='moneyin',
            name='naira',
        ),
        migrations.RemoveField(
            model_name='moneyin',
            name='pound',
        ),
        migrations.RemoveField(
            model_name='moneyout',
            name='dollar',
        ),
        migrations.RemoveField(
            model_name='moneyout',
            name='euro',
        ),
        migrations.RemoveField(
            model_name='moneyout',
            name='naira',
        ),
        migrations.RemoveField(
            model_name='moneyout',
            name='pound',
        ),
        migrations.RemoveField(
            model_name='openingbalance',
            name='dollar',
        ),
        migrations.RemoveField(
            model_name='openingbalance',
            name='euro',
        ),
        migrations.RemoveField(
            model_name='openingbalance',
            name='naira',
        ),
        migrations.RemoveField(
            model_name='openingbalance',
            name='pound',
        ),
        migrations.RemoveField(
            model_name='report',
            name='dollar',
        ),
        migrations.RemoveField(
            model_name='report',
            name='euro',
        ),
        migrations.RemoveField(
            model_name='report',
            name='naira',
        ),
        migrations.RemoveField(
            model_name='report',
            name='pound',
        ),
        migrations.AddField(
            model_name='account',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
        migrations.AddField(
            model_name='closingbalance',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
        migrations.AddField(
            model_name='customerledger',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
        migrations.AddField(
            model_name='generalledger',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
        migrations.AddField(
            model_name='moneyin',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
        migrations.AddField(
            model_name='moneyout',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
        migrations.AddField(
            model_name='openingbalance',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
        migrations.AddField(
            model_name='report',
            name='currencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jamiyafx.currency'),
        ),
    ]