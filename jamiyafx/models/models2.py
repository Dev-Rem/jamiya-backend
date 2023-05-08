import shortuuid
from django.db import models
from .variables import *
from .models1 import *
from shortuuid.django_fields import ShortUUIDField
from datetime import datetime

shortuuid.set_alphabet('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')


class OpeningBalance(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    currencies = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class ClosingBalance(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    currencies = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class Transaction(models.Model):
    customer_name1 = models.CharField(
        verbose_name="Customer Name 1", max_length=1024)
    account_number1 = models.CharField(
        verbose_name="Account Number 1", max_length=10, blank=True)
    bank_name1 = models.CharField(
        verbose_name="Bank Name 1", max_length=100, blank=True)
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
    receipt_number = ShortUUIDField(length=5,
                                    max_length=5,
                                    alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", unique=True, default=shortuuid.ShortUUID().random(length=5))
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]

class Receiving(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='receiving', on_delete=models.CASCADE)
    
    receive_bank_name = models.CharField(
        verbose_name="Bank Name",  max_length=2048, blank=True)
    receive_account_name = models.CharField(
        verbose_name="Account Name",  max_length=2048, blank=True)
    currency_received = models.CharField(
        verbose_name="Currency Recieved",
        choices=CURRENCIES,
        default=DOLLAR,
        max_length=1024,
    )
    cash_received = models.FloatField(
        verbose_name="Cash Recieved", default=0.00)
    receive_mode = models.CharField(
        verbose_name="Receive Mode",
        choices=MODE,
        default=CASH,
        max_length=1024,
    )
    receive_amount_transfered = models.FloatField(
        verbose_name="Amount Transfered", default=0.00, blank=True
    )
    cash_rate = models.FloatField(verbose_name="Cash Rate", default=0.00)
    transfer_rate = models.FloatField(verbose_name="Transfer Rate", default=0.00,  blank=True)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, default=datetime.now
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)
    
class Giving(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='giving', on_delete=models.CASCADE)
    
    give_bank_name = models.CharField(
        verbose_name="Bank Name", max_length=1024, blank=True)
    give_account_name = models.CharField(
        verbose_name="Account Name", max_length=1024, blank=True)
    give_mode = models.CharField(
        verbose_name="Give Mode",
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
    cash_given = models.FloatField(verbose_name="Cash given", default=0.00)
    give_amount_transfered = models.FloatField(
        verbose_name="Amount Transfered", default=0.00, blank=True
    )
    selling_rate = models.FloatField(verbose_name="Selling Rate", default=0.00,  blank=True)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False,default=datetime.now
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)


    
class CustomerLedger(models.Model):
    customer = models.CharField(
        verbose_name="Customer Name", max_length=1024, blank=True
    )
    currencies = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True)
    description = models.TextField(
        verbose_name="Description", null=True, blank=True)
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
    last_updated = models.DateField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class GeneralLedger(models.Model):
    currencies = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True)
    currency_total = models.FloatField(
        verbose_name="Currency Total", default=0.00, blank=True
    )
    grand_total = models.FloatField(
        verbose_name="Grand Total", default=0.00, blank=True
    )
    previous_total = models.FloatField(
        verbose_name="Previous Total", default=0.00, blank=True
    )
    difference = models.FloatField(
        verbose_name="Difference Of Balance", default=0.00, blank=True
    )
    expense = models.FloatField(
        verbose_name="Expenses", default=0.00, blank=True)
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
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]



