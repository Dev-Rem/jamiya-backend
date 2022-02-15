import datetime

from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.models.variables import RECIEVABLE, PAYABLE
from jamiyafx.serializers import *
from jamiyafx.utils import (
    update_closing_bal,
    calculation_for_general_ledger,
    get_customerledger_total,
)

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.


# MoneyIn Model Views
class MoneyInViewSet(viewsets.ModelViewSet):
    queryset = MoneyIn.objects.all()
    serializer_class = MoneyInSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get("pk"))
        report = Report.objects.get(pk=instance.report.pk)

        for i in request.data.keys():
            report.__dict__[i] += request.data[i]
            request.data[i] += instance.__dict__[i]
            report.save()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            update_closing_bal(report=report)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# MoneyOut Model Views
class MoneyOutViewSet(viewsets.ModelViewSet):
    queryset = MoneyOut.objects.all()
    serializer_class = MoneyOutSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get("pk"))
        report = Report.objects.get(pk=instance.report.pk)

        for i in request.data.keys():
            report.__dict__[i] -= request.data[i]
            request.data[i] += instance.__dict__[i]
            report.save()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            update_closing_bal(report=report)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# Rate Model Views
class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def today_rates(self, request):
        rates = Rate.objects.filter(date_created=datetime.date.today())
        serializer = self.get_serializer(rates, many=True)
        return Response(serializer.data)


# CustomerLedger Model Views
class CustomerLedgerViewSet(viewsets.ModelViewSet):
    queryset = CustomerLedger.objects.all()
    serializer_class = CustomerLedgerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get("pk"))
        for i in request.data.keys():
            request.data[i] += instance.__dict__[i]
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get("pk"))
            self.perform_destroy(instance)
            data = calculation_for_general_ledger()
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def ledger_totals(self, request):
        return Response(get_customerledger_total())


# GeneralLedger Model Views
class GeneralLedgerViewSet(viewsets.ModelViewSet):
    queryset = GeneralLedger.objects.all()
    serializer_class = GeneralLedgerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        data = calculation_for_general_ledger(data=request.data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get("pk"))
        for i in request.data.keys():
            request.data[i] += instance.__dict__[i]
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Account Model Views
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get("pk"))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get("pk"))
            self.perform_destroy(instance)
            data = calculation_for_general_ledger()
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Transaction Model View
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        buying_rate = Rate.objects.get(
            date_created=datetime.date.today(),
            currency=request.data["currency_given"],
        ).buying
        if type(request.data) is list:
            for i in request.data:
                i["profit"] = (i["rate"] - buying_rate) * (
                    i["cash_given"] + i["amount_transfered"]
                )
            serializer = self.serializer_class(data=request.data, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            request.data["profit"] = (request.data["rate"] - buying_rate) * (
                request.data["cash_given"] + request.data["amount_transfered"]
            )
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)