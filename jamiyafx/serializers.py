from rest_framework import serializers
from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class MoneyInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyIn
        fields = "__all__"


class MoneyOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyOut
        fields = "__all__"


class OpeningBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningBalance
        fields = "__all__"


class ClosingBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosingBalance
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"


class CustomerLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLedger
        fields = "__all__"


class GeneralLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralLedger
        fields = "__all__"