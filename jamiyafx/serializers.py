from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import serializers
from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *

# serializers for all models


class CurrrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    currencies = CurrrencySerializer()

    class Meta:
        model = Account
        fields = ['id', 'bank_name', 'account_name',
                  'currencies', 'date_created']

    def create(self, validated_data):
        currencies = Currency.objects.create(**validated_data['currencies'])
        del validated_data['currencies']
        account = Account.objects.create(
            currencies=currencies, **validated_data)
        currencies.save()

        return account


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    currencies = CurrrencySerializer()

    class Meta:
        model = Report
        fields = ['id', 'currencies', 'description',
                  'station', 'profit', 'date_created']

    def create(self, validated_data):
        currencies = Currency.objects.create(**validated_data['currencies'])
        del validated_data['currencies']
        report = Report.objects.create(
            currencies=currencies, **validated_data)
        currencies.save()

        return report


class MoneyInSerializer(serializers.ModelSerializer):
    currencies = CurrrencySerializer()

    class Meta:
        model = MoneyIn
        fields = ['id', "report", 'currencies', 'date_created']


class MoneyOutSerializer(serializers.ModelSerializer):
    currencies = CurrrencySerializer()

    class Meta:
        model = MoneyOut
        fields = ['id', "report", 'currencies', 'date_created']


class OpeningBalanceSerializer(serializers.ModelSerializer):
    currencies = CurrrencySerializer()

    class Meta:
        model = OpeningBalance
        fields = ['id', "report", 'currencies', 'date_created']


class ClosingBalanceSerializer(serializers.ModelSerializer):
    currencies = CurrrencySerializer()

    class Meta:
        model = ClosingBalance
        fields = ['id', "report", 'currencies', 'date_created']

class ReceiveGiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiveGive
        fields = "__all__"


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    receive_give = ReceiveGiveSerializer(many=True, read_only=True)
    beneficiaries = BeneficiarySerializer(many=True, read_only=True)
    
    class Meta:
        model = Transaction
        fields = ["id",
            "phone_number",
            "description",
            "initiator",
            "status",
            "category",
            "payment_status",
            "profit",
            "receipt_number",
            "date_created",
            "last_updated", 'receive_give', 'beneficiaries']
        
class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"

class CustomerLedgerSerializer(serializers.ModelSerializer):
    currencies = CurrrencySerializer()

    class Meta:
        model = CustomerLedger
        fields = ['id', "customer", 'description',
                  'status', 'currencies', 'date_created']

    def create(self, validated_data):
        currencies = Currency.objects.create(**validated_data['currencies'])
        del validated_data['currencies']
        obj = CustomerLedger.objects.create(
            currencies=currencies, **validated_data)
        currencies.save()
        return obj

class GeneralLedgerSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralLedger
        fields = [
            "currencies",
            "currency_total",
            "grand_total",
            "previous_total",
            "difference",
            "expense",
            "book_profit",
            "calculated_profit",
            "variance",
            'date_created'
        ]
