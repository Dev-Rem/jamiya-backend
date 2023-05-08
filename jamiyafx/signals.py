import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.exceptions import ObjectDoesNotExist

from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.utils import (
    calculation_for_general_ledger,
    update_closing_and_account_bal)
from jamiyafx.transactionHandler import TransactionHandler


@receiver(post_save, sender=Report)
def create_complete_report(sender, instance, created, **kwargs):

    if created:

        # # Create money in object and attach it to report (instance)
        money_in_currencies = Currency.objects.create()
        MoneyIn.objects.create(report=instance, currencies=money_in_currencies)

        # # Create money out object and attach it to report (instance)
        money_out_currencies = Currency.objects.create()
        MoneyOut.objects.create(
            report=instance, currencies=money_out_currencies)

        # # Create closing balance object and attach it to report (instance)
        closing_balance_currencies = Currency.objects.create()
        ClosingBalance.objects.create(
            report=instance, currencies=closing_balance_currencies)

        # # Create opening balance object and attach it to report (instance)
        opening_balance_currencies = Currency.objects.create()
        opening_bal = OpeningBalance.objects.create(
            report=instance, currencies=opening_balance_currencies)

        previous_report = Report.objects.filter(
            station=instance.station).order_by('-date_created')[1]

        # Get previous report closing balance
        previous_closing_bal = ClosingBalance.objects.get(
            report=previous_report)

        # Assign previous day closing balance to current(instance) opening balance
        instance.currencies.naira = opening_bal.currencies.naira = previous_closing_bal.currencies.naira
        instance.currencies.dollar = opening_bal.currencies.dollar = previous_closing_bal.currencies.dollar
        instance.currencies.pound = opening_bal.currencies.pound = previous_closing_bal.currencies.pound
        instance.currencies.euro = opening_bal.currencies.euro = previous_closing_bal.currencies.euro


        # update closing balance
        opening_bal.currencies.save()
        update_closing_and_account_bal(instance)
        instance.currencies.save()


