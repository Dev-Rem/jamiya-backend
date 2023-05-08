from django.contrib import admin
from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *

# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "account_name")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "status", "station", "salary")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("station",  'date_created')


@admin.register(MoneyIn)
class MoneyInAdmin(admin.ModelAdmin):
    list_display = ("report", "currencies",  "date_created")


@admin.register(MoneyOut)
class MoneyOutAdmin(admin.ModelAdmin):
    list_display = ("report", "currencies", "date_created")


@admin.register(OpeningBalance)
class OpeningBalanceAdmin(admin.ModelAdmin):
    list_display = ("report", "currencies", "date_created")


@admin.register(ClosingBalance)
class ClosingBalanceAdmin(admin.ModelAdmin):
    list_display = ("report", "currencies", "date_created")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number",
        "initiator",
    )

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display =('transaction', 'customer_account_name', 'customer_account_number', 'customer_bank_name')
    
@admin.register(ReceiveGive)
class ReceiveGiveAdmin(admin.ModelAdmin):
    list_display=( 'transaction','currency', 'mode')
    

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("currency", "buying", "selling", "date_created")


@admin.register(CustomerLedger)
class CustomerLedgerAdmin(admin.ModelAdmin):
    list_display = ("customer", "currencies", "status")


@admin.register(GeneralLedger)
class GeneralLedgerAdmin(admin.ModelAdmin):
    list_display = (
        "calculated_profit", "variance", "currencies", "date_created")


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "phone_number", "receipt")


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('naira', "dollar", "pound", "euro", "date_created")
