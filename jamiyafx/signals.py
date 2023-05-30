import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.exceptions import ObjectDoesNotExist

from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.utils import (
    update_closing_and_account_bal)


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
        instance.currencies.ngn = opening_bal.currencies.ngn = previous_closing_bal.currencies.ngn
        instance.currencies.usd = opening_bal.currencies.usd = previous_closing_bal.currencies.usd
        instance.currencies.gbp = opening_bal.currencies.gbp = previous_closing_bal.currencies.gbp
        instance.currencies.eur = opening_bal.currencies.eur = previous_closing_bal.currencies.eur


        # update closing balance
        opening_bal.currencies.save()
        update_closing_and_account_bal(instance)
        instance.currencies.save()


