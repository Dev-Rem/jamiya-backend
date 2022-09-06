from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import serializers
from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *

# serializers for all models


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class MoneyInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyIn
        fields = "__all__"


class MoneyOutSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoneyOut
        fields = "__all__"


class OpeningBalanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpeningBalance
        fields = "__all__"


class ClosingBalanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClosingBalance
        fields = "__all__"


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class RateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"


class CustomerLedgerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerLedger
        fields = "__all__"


class GeneralLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralLedger
        fields = "__all__"
