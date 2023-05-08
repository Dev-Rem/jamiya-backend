import datetime
from django.db import models
from .variables import *

# Create your models here.


class Currency(models.Model):
    naira = models.FloatField(verbose_name="Naira Balance", default=0.00)
    dollar = models.FloatField(verbose_name="Dollar Balance", default=0.00)
    pound = models.FloatField(verbose_name="Pound Balance", default=0.00)
    euro = models.FloatField(verbose_name="Euro Balance", default=0.00)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class Rate(models.Model):
    currency = models.CharField(
        verbose_name="Station", max_length=30, choices=CURRENCIES, default=DOLLAR
    )
    buying = models.FloatField(verbose_name="Buying Rate", default=0.00)

    selling = models.FloatField(verbose_name="Selling Rate", default=0.00)

    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class Account(models.Model):
    bank_name = models.CharField(verbose_name="Bank Name", max_length=1024)
    account_name = models.CharField(
        verbose_name="Account Name", max_length=1024
    )
    currencies = models.OneToOneField(
        Currency, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class Employee(models.Model):
    name = models.CharField(verbose_name="Full Nmae", max_length=1024)
    address = models.TextField(verbose_name="Address", max_length=1024)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=15)
    salary = models.FloatField(verbose_name="Salary", default=0.00)
    status = models.CharField(
        verbose_name="Status", max_length=50, choices=EMPLOYEE_STATUS, default=ACTIVE
    )
    station = models.CharField(
        verbose_name="Station", max_length=30, choices=EMPLOYEE_STATIONS, default=INTERN
    )
    date_joined = models.DateTimeField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_joined"]


class Report(models.Model):
    currencies = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True)
    description = models.CharField(verbose_name="Description", max_length=1024)
    station = models.CharField(
        verbose_name="Station",
        max_length=30,
        choices=EMPLOYEE_STATIONS,
        default=FRONTDESK,
    )
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    profit = models.FloatField(
        verbose_name="Calculated Profit", default=0.0, blank=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-date_created"]


class MoneyIn(models.Model):
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


class MoneyOut(models.Model):
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


class Receipt(models.Model):
    customer_name = models.CharField(
        verbose_name="Customer Name", max_length=1024)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=15)
    receipt = models.FileField(
        verbose_name="Receipt", upload_to="receipts/"
    )
    date_created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name="Date Last Updated", auto_now=True)
