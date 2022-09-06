import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.utils import (
    calculation_for_general_ledger,
    update_closing_bal,
    TransactionHandler,
)


@receiver(post_save, sender=Report)
def create_complete_report(sender, instance, created, **kwargs):
    if created:

        # Create money in object and attach it to report (instance)
        MoneyIn.objects.create(report=instance)

        # Create money out object and attach it to report (instance)
        MoneyOut.objects.create(report=instance)

        # Create closing balance object and attach it to report (instance)
        ClosingBalance.objects.create(report=instance)

        # Create opening balance object and attach it to report (instance)
        opening_bal = OpeningBalance.objects.create(report=instance)

        # try get previous report from appropriate day
        try:
            # Check that the day is Monday and get previous report from previous week
            if datetime.datetime.today().weekday() == 0:
                previous_report = Report.objects.get(
                    station=instance.station,
                    date_created=datetime.datetime.today() - datetime.timedelta(days=3),
                )
            # else get previous day report
            else:
                previous_report = Report.objects.get(
                    station=instance.station,
                    date_created=datetime.datetime.today() - datetime.timedelta(days=1),
                )

        except ObjectDoesNotExist:
            previous_report = Report.objects.all()[1]

        # Get previous report closing balance
        previous_closing_bal = ClosingBalance.objects.get(
            report=previous_report)

        # Assign previous day closing balance to current (instance) opening balance
        instance.naira = opening_bal.naira = previous_closing_bal.naira
        instance.dollar = opening_bal.dollar = previous_closing_bal.dollar
        instance.pound = opening_bal.pound = previous_closing_bal.pound
        instance.euro = opening_bal.euro = previous_closing_bal.euro
        opening_bal.save()
        # update closing balance
        update_closing_bal(instance)
        instance.save()


# signal function to update report and account based on changes
@receiver(post_save, sender=Transaction)
def update_report_and_account(sender, instance, created, **kwargs):
    if created:
        transaction_handler = TransactionHandler(instance)
        if instance.recieve_mode == CASH and instance.give_mode == CASH:
            transaction_handler.recieve_cash_give_cash()
            data = calculation_for_general_ledger()
            data.save()
        elif instance.recieve_mode == CASH and instance.give_mode == TRANSFER:
            transaction_handler.recieve_cash_do_transfer()
            data = calculation_for_general_ledger()
            data.save()
        elif instance.recieve_mode == TRANSFER and instance.give_mode == TRANSFER:
            transaction_handler.recieve_transfer_do_transfer()
            data = calculation_for_general_ledger()
            data.save()
        elif instance.recieve_mode == TRANSFER and instance.give_mode == CASH:
            transaction_handler.recieve_transfer_give_cash()
            data = calculation_for_general_ledger()
            data.save()
