import datetime

from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.serializers import *
from jamiyafx.utils import (
    update_closing_bal,
    calculation_for_general_ledger,
    get_customerledger_total,
)
from jamiyafx.models.variables import SALES

from decouple import config
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
CACHE_TTL = int(config("CACHE_TTL"))

# MoneyIn Model Views


class MoneyInViewSet(viewsets.ModelViewSet):
    queryset = MoneyIn.objects.all()
    serializer_class = MoneyInSerializer
    permission_classes = [IsAuthenticated]

    # cache all list requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # # cache all retrieve requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # get the report which the money in object is attached to.
        instance = self.queryset.get(pk=kwargs.get("pk"))
        report = Report.objects.get(pk=instance.report.pk)

        # update the report
        for i in request.data.keys():
            report.__dict__[i] += request.data[i]
            request.data[i] += instance.__dict__[i]
            report.save()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # update report closing balance
            update_closing_bal(report=report)
            # run the calculation for the general ledger because of update to report
            data = calculation_for_general_ledger()
            data.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# MoneyOut Model Views
class MoneyOutViewSet(viewsets.ModelViewSet):
    queryset = MoneyOut.objects.all()
    serializer_class = MoneyOutSerializer
    permission_classes = [IsAuthenticated]

    # cache all list requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # cache all retrieve requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get("pk"))
        report = Report.objects.get(pk=instance.report.pk)

        # update the report
        for i in request.data.keys():
            report.__dict__[i] -= request.data[i]
            request.data[i] += instance.__dict__[i]
            report.save()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # update report closing balance
            update_closing_bal(report=report)
            # run the calculation for the general ledger because of update to report
            data = calculation_for_general_ledger()
            data.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# Rate Model Views
class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated]

    # cache all list requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # cache all retrieve requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # create new rate for the day
    def create(self, request, *args, **kwargs):
        serializer = RateSerializer(
            data=request.data, many=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # update individual rates
    def partial_update(self, request, *args, **kwargs):
        # get the instance to be updated
        instance = self.queryset.get(pk=kwargs.get("pk"))
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # run calculation for general ledger because of rate change
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # cache requests to this function
    # this function is to get all the rates for the day
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    @action(detail=False)
    def today_rates(self, request):
        # get rates for the day
        today_rates = Rate.objects.filter(date_created=datetime.date.today())
        # check is they exists and return it
        if today_rates:
            serializer = self.get_serializer(
                today_rates, many=True, context={"request": request}
            )
            return Response(serializer.data)
        return Response({"status": "There are no rates for today"})


# CustomerLedger Model Views
class CustomerLedgerViewSet(viewsets.ModelViewSet):
    queryset = CustomerLedger.objects.all()
    serializer_class = CustomerLedgerSerializer
    permission_classes = [IsAuthenticated]

    # cache all list requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # cache all retrieve requests
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # create a new customer ledger
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # calculate general ledger because of customer ledger change
            # data = calculation_for_general_ledger()
            # data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    # partial update to customer ledger update
    def partial_update(self, request, *args, **kwargs):
        # get instance for update
        instance = self.queryset.get(pk=kwargs.get("pk"))
        # perform update
        for i in request.data.keys():
            request.data[i] += instance.__dict__[i]
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # calculate general ledger because of customer ledger change
            # data = calculation_for_general_ledger()
            # data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete a customer ledger
    def destroy(self, request, *args, **kwargs):
        # try to delete instance if it exist and throw exception if it doesn't
        try:
            instance = self.queryset.get(pk=kwargs.get("pk"))
            self.perform_destroy(instance)
            # calculate general ledger because of customer ledger change
            data = calculation_for_general_ledger()
            data.save()
            return Response(
                {"status": "Delete Successful"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # this is a function to get the currency totals of all customer ledgers
    @ action(detail=False)
    def ledger_totals(self, request):
        return Response(get_customerledger_total())


# GeneralLedger Model Views
class GeneralLedgerViewSet(viewsets.ModelViewSet):
    queryset = GeneralLedger.objects.all()
    serializer_class = GeneralLedgerSerializer
    permission_classes = [IsAuthenticated]

    # cache all list requests
    @ method_decorator(vary_on_cookie)
    @ method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # cache all retrieve request
    @ method_decorator(vary_on_cookie)
    @ method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # create new general ledger report
    def create(self, request, *args, **kwargs):
        # get instance of the last general ledger object created
        instance = GeneralLedger.objects.last()
        # check if instance exists or if the last instance was created on present day
        if (instance == None) or (datetime.date.today() != instance.date_created):
            # send data for calculationa and then serialize the results
            data = calculation_for_general_ledger(data=request.data)
            serializer = self.serializer_class(
                data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "Already created report for today"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # partial update of a general ledger instance
    def partial_update(self, request, *args, **kwargs):
        # get instance to be updated
        instance = self.queryset.get(pk=kwargs.get("pk"))
        # perform update
        for i in request.data.keys():
            request.data[i] += instance.__dict__[i]
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # calculate general ledger becuase of update made
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Account Model Views
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    # cache all list requests
    @ method_decorator(vary_on_cookie)
    @ method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # cache all retrieve request
    @ method_decorator(vary_on_cookie)
    @ method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # partial update to an account instance
    def partial_update(self, request, *args, **kwargs):
        # get instance to be updated
        instance = self.queryset.get(pk=kwargs.get("pk"))
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # calculate general ledger because of changes to the instance
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete an account instance
    def destroy(self, request, *args, **kwargs):
        # try to delete the instance if it exists and throw exception if it doesn't
        try:
            # get instance to be deleted
            instance = self.queryset.get(pk=kwargs.get("pk"))
            self.perform_destroy(instance)
            # calculate general ledger because of deleted account
            data = calculation_for_general_ledger()
            data.save()
            return Response({"status": "Delete Successful"}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Transaction Model View
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    # cache all list request
    @ method_decorator(vary_on_cookie)
    @ method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # cache all retrieve requests
    @ method_decorator(vary_on_cookie)
    @ method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # create a new transaction
    def create(self, request, *args, **kwargs):
        # Get the recent buying rate
        buying_rate = Rate.objects.get(
            date_created=datetime.date.today(),
            currency=request.data["currency_given"],
        ).buying

        # Check if multiple transactions were posted
        if (type(request.data) is list):
            serializer = self.serializer_class(
                data=request.data, many=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Check if transaction is a sales transaction
        elif request.data['categories'] == SALES:
            # calculate sales profit of the transaction
            request.data["profit"] = (
                request.data["rate"] - buying_rate) * request.data['amount_recieved']
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else if it is a normal purchase transaction
        else:
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Report Model views
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    # cache all list requests
    @ method_decorator(vary_on_cookie)
    @ method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # create new report
    def create(self, request, *args, **kwargs):
        # get instance of the last report created by the work station
        instance = Report.objects.get(station=request.data['station'])
        # check if instance exists or if the report was created on present day
        if (instance == None) or (datetime.date.today() != instance.date_created):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "Already created report for today"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # this function is to return all the variablesa and their values that make up a complete report
    # @method_decorator(vary_on_cookie)
    # @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        print("using this view")
        instance = self.queryset.get(pk=kwargs.get("pk"))
        report_serializer = ReportSerializer(
            instance, context={"request": request})

        money_in = MoneyIn.objects.get(report=instance)
        money_in_serializer = MoneyInSerializer(
            money_in, context={"request": request})

        money_out = MoneyOut.objects.get(report=instance)
        money_out_serializer = MoneyOutSerializer(
            money_out, context={"request": request}
        )

        opening_bal = OpeningBalance.objects.get(report=instance)
        opening_bal_serializer = OpeningBalanceSerializer(
            opening_bal, context={"request": request}
        )

        closing_bal = ClosingBalance.objects.get(report=instance)
        closing_bal_serializer = ClosingBalanceSerializer(
            closing_bal, context={"request": request}
        )

        data = {
            "report": report_serializer.data,
            "money_in": money_in_serializer.data,
            "money_out": money_out_serializer.data,
            "opening_balance": opening_bal_serializer.data,
            "closing_balance": closing_bal_serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)
