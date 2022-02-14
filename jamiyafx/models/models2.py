import datetime
from django.db import models
from .variables import *
from .models1 import *


class OpeningBalance(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    naira = models.FloatField(verbose_name="Naira Balance", default=0.00)
    dollar = models.FloatField(verbose_name="Dollar Balance", default=0.00)
    pound = models.FloatField(verbose_name="Pound Balance", default=0.00)
    euro = models.FloatField(verbose_name="Euro Balance", default=0.00)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class ClosingBalance(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    naira = models.FloatField(verbose_name="Naira Balance", default=0.00)
    dollar = models.FloatField(verbose_name="Dollar Balance", default=0.00)
    pound = models.FloatField(verbose_name="Pound Balance", default=0.00)
    euro = models.FloatField(verbose_name="Euro Balance", default=0.00)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class Transaction(models.Model):
    beneficiaries = models.CharField(
        verbose_name="beneficiaries",
        max_length=30,
        choices=PAYMENT,
        default=SINGLE_PAYMENT,
    )
    customer_name1 = models.CharField(verbose_name="Customer Name 1", max_length=1024)
    account_number1 = models.CharField(verbose_name="Account Number 1", max_length=10)
    bank_name1 = models.CharField(verbose_name="Bank Name 1", max_length=100)
    customer_name2 = models.CharField(
        verbose_name="Customer Name 2", max_length=1024, blank=True
    )
    account_number2 = models.CharField(
        verbose_name="Account Number 2", max_length=10, blank=True
    )
    bank_name2 = models.CharField(
        verbose_name="Bank Name 2", max_length=100, blank=True
    )

    phone_number = models.CharField(verbose_name="Phone Number", max_length=15)
    address = models.TextField(verbose_name="Address", max_length=1024)
    transfered_to = models.CharField(
        verbose_name="Transfered To",
        max_length=50,
        choices=BANKS,
        default=PROVIDUS_BANK,
        null=True,
    )
    currency_recieved = models.CharField(
        verbose_name="Currency Recieved",
        choices=CURRENCIES,
        default=DOLLAR,
        max_length=1024,
    )
    amount_recieved = models.FloatField(verbose_name="Amount Recieved", default=0.00)
    recieve_mode = models.CharField(
        verbose_name="How Money was Recieved",
        choices=MODE,
        default=CASH,
        max_length=1024,
    )
    rate = models.FloatField(verbose_name="Rate of Exchange", default=0.00)
    give_mode = models.CharField(
        verbose_name="How Money was given",
        choices=MODE,
        default=CASH,
        max_length=1024,
    )
    currency_given = models.CharField(
        verbose_name="Currency Recieved",
        choices=CURRENCIES,
        default=DOLLAR,
        max_length=1024,
    )
    cash_given = models.FloatField(verbose_name="Amount given", default=0.00)
    amount_transfered = models.FloatField(
        verbose_name="Amount Transfered", default=0.00, blank=True
    )
    description = models.CharField(verbose_name="Description", max_length=1024)
    initiator = models.CharField(
        verbose_name="Station",
        max_length=30,
        choices=EMPLOYEE_STATIONS,
        default=FRONTDESK,
    )
    status = models.CharField(
        verbose_name="Tansaction Status",
        choices=TRANSACTION_STATUS,
        default=SENT,
        max_length=1024,
    )
    category = models.CharField(
        verbose_name="Category of Transaction",
        choices=CATEGORIES,
        default=PURCHASE,
        max_length=1024,
    )
    profit = models.FloatField(
        verbose_name="Calculated Profit", default=0.0, blank=True
    )
    paid_from = models.CharField(
        verbose_name="Payment From", max_length=50, choices=BANKS, default=ZENITH_BANK, null=True
    )
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(verbose_name="Date Last Updated", auto_now=True)

    @property
    def receipt_number(self):
        return "{}/00{}".format(self.initiator, self.pk)

    class Meta:
        ordering = ["-date_created"]


class CustomerLedger(models.Model):
    customer = models.CharField(
        verbose_name="Customer Name", max_length=1024, blank=True
    )
    naira = models.FloatField(verbose_name="Naira Balance", default=0.00)
    dollar = models.FloatField(verbose_name="Dollar Balance", default=0.00)
    pound = models.FloatField(verbose_name="Pound Balance", default=0.00)
    euro = models.FloatField(verbose_name="Euro Balance", default=0.00)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    status = models.CharField(
        verbose_name="Status of Payment",
        choices=DEBTORS,
        max_length=1024,
        default=RECIEVABLE,
        null=True,
    )

    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class GeneralLedger(models.Model):
    naira = models.FloatField(verbose_name="Naira Balance", default=0.00, blank=True)
    dollar = models.FloatField(verbose_name="Dollar Balance", default=0.00, blank=True)
    pound = models.FloatField(verbose_name="Pound Balance", default=0.00, blank=True)
    euro = models.FloatField(verbose_name="Euro Balance", default=0.00, blank=True)
    currency_total = models.FloatField(
        verbose_name="Currency Total", default=0.00, blank=True
    )
    grand_total = models.FloatField(
        verbose_name="Grand Total", default=0.00, blank=True
    )
    difference = models.FloatField(
        verbose_name="Difference Of Balance", default=0.00, blank=True
    )
    expense = models.FloatField(verbose_name="Expenses", default=0.00, blank=True)
    book_profit = models.FloatField(
        verbose_name="Book Profit", default=0.00, blank=True
    )
    calculated_profit = models.FloatField(
        verbose_name="Calculated Profit", default=0.00, blank=True
    )
    variance = models.FloatField(
        verbose_name="Ledger Variance", default=0.00, blank=True
    )

    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]