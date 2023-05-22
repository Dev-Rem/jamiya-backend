import json
from datetime import datetime, timedelta
from datetime import date

from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.serializers import *
from jamiyafx.utils import *
from jamiyafx.transactionHandler import TransactionHandler

from jamiyafx.models.variables import SALES

from decouple import config
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.decorators import action
from rest_framework import viewsets, status,filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# MoneyIn Model Views

class MyPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page

class MoneyInViewSet(viewsets.ModelViewSet):
    queryset = MoneyIn.objects.all()
    serializer_class = MoneyInSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # get the report which the money in object is attached to.
        report = Report.objects.get(pk=kwargs.get("pk"))
        instance = self.queryset.get(report=report)

        # update the report
        for i in request.data.keys():
            report.currencies.__dict__[i] += request.data[i]
            request.data[i] += instance.currencies.__dict__[i]
            report.currencies.save()
        currency_serializer = CurrrencySerializer(
            instance.currencies, data=request.data, partial=True, context={'request': request})
        serializer = self.serializer_class(instance)
        if currency_serializer.is_valid(raise_exception=True):
            currency_serializer.save()
            # update report closing balance
            update_closing_and_account_bal(report=report)
            # run the calculation for the general ledger because of update to report
            data = calculation_for_general_ledger()
            data.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# MoneyOut Model Views
class MoneyOutViewSet(viewsets.ModelViewSet):
    queryset = MoneyOut.objects.all()
    serializer_class = MoneyOutSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        report = Report.objects.get(pk=kwargs.get("pk"))
        instance = self.queryset.get(report=report)
        # update the report
        for i in request.data.keys():
            report.currencies.__dict__[i] -= request.data[i]
            request.data[i] += instance.currencies.__dict__[i]
            report.currencies.save()
        currency_serializer = CurrrencySerializer(
            instance.currencies, data=request.data, partial=True, context={'request': request})
        serializer = self.serializer_class(instance)
        if currency_serializer.is_valid(raise_exception=True):
            currency_serializer.save()
            # update report closing balance
            update_closing_and_account_bal(report=report)
            # run the calculation for the general ledger because of update to report
            data = calculation_for_general_ledger()
            data.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# Rate Model Views
class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
    def update(self, request, *args, **kwargs):
        # get the instance to be updated
        instance = Rate.objects.get(currency=request.data['currency'])
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # run calculation for general ledger because of rate change
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def today_rates(self, request):
        # get rates for the day
        today_rates = Rate.objects.filter(date_created=date.today())
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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # create a new customer ledger
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # calculate general ledger because of customer ledger change
            data = calculation_for_general_ledger()
            data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    # partial update to customer ledger update
    def partial_update(self, request, *args, **kwargs):
        # get instance for update
        instance = self.queryset.get(pk=kwargs.get("pk"))
        print(instance.currencies)
        print(request.data['currencies'])
        # perform update
        currency_serializer = CurrrencySerializer(
            instance.currencies, data=request.data['currencies'], partial=True, context={'request': request})
        serializer = self.serializer_class()
        if currency_serializer.is_valid(raise_exception=True):
            currency_serializer.save()
            # calculate general ledger because of customer ledger change
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete a customer ledger
    def destroy(self, request, *args, **kwargs):
        # try to delete instance if it exist and throw exception if it doesn't
        try:
            instance = self.queryset.get(pk=kwargs.get("pk"))
            instance.currencies.delete()
            self.perform_destroy(instance)
            # calculate general ledger because of customer ledger change
            data = calculation_for_general_ledger()
            data.save()
            return Response(
                {"status": "Delete Successful"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# GeneralLedger Model Views
class GeneralLedgerViewSet(viewsets.ModelViewSet):
    queryset = GeneralLedger.objects.all()
    serializer_class = GeneralLedgerSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # create new general ledger report
    def create(self, request, *args, **kwargs):
        # get instance of the last general ledger object created
        instance = GeneralLedger.objects.order_by('-date_created').first()
        serializer = GeneralLedgerSerializer(instance)
        # check if instance exists or if the last instance was created on present day
        if (instance == None) or (date.today() != instance.date_created):
            # send data for calculationa and then serialize the results
            data = calculation_for_general_ledger(data=request.data)
            serializer = self.serializer_class(
                data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        data = calculation_for_general_ledger()
        data.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = GeneralLedger.objects.order_by('-date_created').first()
            serializer = self.serializer_class(instance=instance)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "You have not created report"}, status=status.HTTP_400_BAD_REQUEST)
            
        
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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if Account.objects.filter(bank_name=request.data['bank_name'], account_name=request.data['account_name']).exists():
            return Response({'message': 'Account already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Currency.objects.create(
                **request.data['currencies'])
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = calculation_for_general_ledger()
                data.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    # partial update to an account instance

    def partial_update(self, request, *args, **kwargs):
        # get instance to be updated
        instance = self.queryset.get(pk=kwargs.get("pk"))

        currency_serializer = CurrrencySerializer(
            instance.currencies, data=request.data, partial=True, context={'request': request}
        )
        serializer = self.serializer_class(instance)
        if currency_serializer.is_valid(raise_exception=True):
            currency_serializer.save()
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
            currencies = Currency.objects.get(id=instance.currencies.id)

            currencies.delete()
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_created', 'initiator', 'description', 'receipt_number', 'category', 'payment_status']
    pagination_class = MyPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    
    # create a new transaction
    def create(self, request, *args, **kwargs):
        print(request.data)
            # Check if transaction is a sales transaction
        if request.data['category'] == PURCHASE:
            data = request.data
            receive_give = data.pop('receive_give')
            beneficiaries = data.pop('beneficiaries')
            
            serializer = self.serializer_class(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                create_beneficiary_receiving_and_giving(receive_give=receive_give, transaction=instance, beneficiaries=beneficiaries)
                transaction_handler = TransactionHandler(instance)
                transaction_handler.handle_receive_give()
                data = calculation_for_general_ledger()
                data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        elif request.data['category'] == SALES or request.data['category'] == CROSS_CURRENCY:
        
            data = request.data
            receive_give = data.pop('receive_give')
            beneficiaries = data.pop('beneficiaries')
            
            serializer = self.serializer_class(data=data, context={'request': request})
            profit = calc_profit_for_sales(receive_give)
            print(profit)
            serializer.initial_data['profit'] = profit
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                create_beneficiary_receiving_and_giving(receive_give=receive_give, transaction=instance, beneficiaries=beneficiaries)
                transaction_handler = TransactionHandler(instance)
                transaction_handler.handle_receive_give()
                data = calculation_for_general_ledger()
                data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
            instance = self.queryset.get(receipt_number=request.data['receipt_number'])
            
            transaction_handler = TransactionHandler(instance=instance)
            transaction_handler.reverse_transaction()
            
            create_beneficiary_receiving_and_giving(receive_give=request.data['receive_give'], transaction=instance, beneficiaries=request.data['beneficiaries'])
            
            transaction_handler.handle_receive_give()
            data = calculation_for_general_ledger()
            data.save()
            
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(receipt_number=request.data['receipt_number'])
            
            transaction_handler = TransactionHandler(instance=instance)
            transaction_handler.reverse_transaction()
            instance.beneficiaries.all().delete()
            self.perform_destroy(instance)
            # calculate general ledger because of deleted account
            data = calculation_for_general_ledger()
            data.save()
            return Response({"status": "Delete Successful"}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        
# Report Model views
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_created', 'station', 'description']
    pagination_class = MyPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # create new report
    def create(self, request, *args, **kwargs):
        # get instance of the last report created by the work station
        instance = Report.objects.filter(
            station=request.data['station']).order_by('-date_created').first()
        serializer = ReportSerializer(instance)
        # check if instance exists or if the report was created on present day
        if (instance == None) or (date.today() != instance.date_created):
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
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