from django.contrib import admin
from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *

# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "account_name", "naira", "dollar", "pound", "euro")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "status", "station", "salary")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("station", "naira", "dollar", "pound", "euro")


@admin.register(MoneyIn)
class MoneyInAdmin(admin.ModelAdmin):
    list_display = ("report", "naira", "dollar", "pound", "euro", "date_created")


@admin.register(MoneyOut)
class MoneyOutAdmin(admin.ModelAdmin):
    list_display = ("report", "naira", "dollar", "pound", "euro", "date_created")


@admin.register(OpeningBalance)
class OpeningBalanceAdmin(admin.ModelAdmin):
    list_display = ("report", "naira", "dollar", "pound", "euro", "date_created")


@admin.register(ClosingBalance)
class ClosingBalanceAdmin(admin.ModelAdmin):
    list_display = ("report", "naira", "dollar", "pound", "euro", "date_created")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name1",
        "account_number1",
        "bank_name1",
        "cash_given",
        "amount_transfered",
        "initiator",
    )


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("currency", "buying", "selling", "date_created")


@admin.register(CustomerLedger)
class CustomerLedgerAdmin(admin.ModelAdmin):
    list_display = ("customer", "naira", "dollar", "pound", "euro", "status")


@admin.register(GeneralLedger)
class GeneralLedgerAdmin(admin.ModelAdmin):
    list_display = ("naira", "dollar", "pound", "euro", "calculated_profit", "variance")


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "phone_number", "receipt")
