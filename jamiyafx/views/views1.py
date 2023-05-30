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

    # This MoneyInViewSet partial_update is used for editing an alerady created money in object
    def partial_update(self, request, *args, **kwargs):
        """This money in partial_update function updates a money in based on the report
        it actually just updates the currency object of the money in object

        Args:
            request (PATCH): report id required NOT money in id

        Returns:
            serializer.data: returns serialized version of the updated money in object
        """
        # get the report which the money in object is attached to
        report = Report.objects.get(pk=kwargs.get("pk"))
        # get the instance of the money in based on the report
        instance = self.queryset.get(report=report)

        # add the values from the instance to the values in the request data
        for i in request.data.keys():
            request.data[i] += instance.currencies.__dict__[i]
            
        # update the money in currency object with the serializer
        currency_serializer = CurrrencySerializer(
            instance.currencies, data=request.data, partial=True, context={'request': request})
        # serialize the money in instance
        serializer = self.serializer_class(instance)
        
        if currency_serializer.is_valid(raise_exception=True):
            currency_serializer.save()
            # update report, closing balances and account
            update_closing_and_account_bal(report=report)
            # calculate for the general ledger 
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
        """This money out partial_update function updates a money out based on the report
        it actually just updates the currency object of the money out object

        Args:
            request (PATCH): report id required NOT money out id

        Returns:
            serializer.data: returns serialized version of the updated money out object
        """
        # get the report which the money in object is attached to
        report = Report.objects.get(pk=kwargs.get("pk"))
        # get the instance of the money in based on the report
        instance = self.queryset.get(report=report)
        
        # add the values from the instance to the values in the request data
        for i in request.data.keys():
            request.data[i] += instance.currencies.__dict__[i]
            
        # update the money in currency object with the serializer
        currency_serializer = CurrrencySerializer(
            instance.currencies, data=request.data, partial=True, context={'request': request})
        # serialize the money out instance
        serializer = self.serializer_class(instance)
        if currency_serializer.is_valid(raise_exception=True):
            currency_serializer.save()
            # update report, closing balances, account
            update_closing_and_account_bal(report=report)
            # calculate for the general ledger 
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

    def create(self, request, *args, **kwargs):
        """This create function will not really be used too often because i have adjusted
        the code to use only one rate.

        Args:
            request (POST): send a post request along with data

        Returns:
            json: details of the rate created
        """
        serializer = RateSerializer(
            data=request.data, many=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # update individual rates
    def update(self, request, *args, **kwargs):
        """this update function is used to update a particular rate based on currency
        you dont have to send the rate id you want to update so you can put any number for id 
        because the ModelViewSet put function requires it.

        Args:
            request (PUT): send rate data in json

        Returns:
            json: serialized updated rate
        """
        # get the instance to be updated based on currency NOT id
        instance = Rate.objects.get(currency=request.data['currency'])
        # update rate using serializer
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # calculate general ledger
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        """ creates new customer ledger 

        Args:
            request (POST): send a json with the required customerledger fields

        Returns:
            json: serialized customer ledger creates
        """
        # create customer ledger using serializer
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # calculate general ledger
            data = calculation_for_general_ledger()
            data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    # partial update to customer ledger update
    def partial_update(self, request, *args, **kwargs):
        """updates the currency object of the customer ledger according to data provided

        Args:
            request (PATCH): JSON containing the required customer ledger field and currency
            also customer ledger id required

        Returns:
            JSON: serialized object of the updated customer ledger along with it underlying currency object
        """
        # get instance for update
        instance = self.queryset.get(pk=kwargs.get("pk"))
        # perform update on customer ledger currency object using serializer
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
        """deletes a customer ledger object along with its underlying currency object

        Args:
            request (DELETE): customer ledger id required

        Returns:
            JSON: a json with status delete successful
        """
        # try to delete instance if it exist and throw exception if it doesn't
        try:
            # get instance to be deleted
            instance = self.queryset.get(pk=kwargs.get("pk"))
            # delete underlying currency object
            instance.currencies.delete()
            # delete customerledger
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
    pagination_class = MyPagination
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # create new general ledger report
    def create(self, request, *args, **kwargs):
        """creates a general ledger object but firsts get the last object created 
        and check the date it was created

        Args:
            request (POST): a json with all required fields set to 0

        Returns:
            JSON: serialized json of the created or fetched general ledger object
        """
        # get instance of the last general ledger object created
        instance = GeneralLedger.objects.order_by('-date_created').first()
        # serializer the instance
        serializer = GeneralLedgerSerializer(instance)
        # check if instance exists or if the last instance was created on present day
        if (instance == None) or (date.today() != instance.date_created):
            # send data for calculation and then create object using serializer
            data = calculation_for_general_ledger(data=request.data)
            serializer = self.serializer_class(
                data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # calculate general ledger
        data = calculation_for_general_ledger()
        data.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
    # this retrieve function is updated to get the last object created
    def retrieve(self, request, *args, **kwargs):
        """this is a basic retrieve function but i do not think i use

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
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
        # check if account already exists if it exists returned message
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
        """deletes a account but firsts deletes in currency instance

        Args:
            request (DELETE): account id required

        Returns:
            message: deletion succesful
        """
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
        """lists all transactions based on the pagination settings

        Args:
            request (GET): just send a GET request to /transactions/

        Returns:
            reports: list of all transactions
        """
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    
    # create a new transaction
    def create(self, request, *args, **kwargs):
        """This create function creates transaction and also calculate profit when transaction is either sales of cross currency

        Args:
            request (POST): data should be sent along with the beneficiaries and receive_give data

        Returns:
            serializer.data: Created transaction
        """
        # Check if transaction is a purchase transaction
        data = request.data
        # pop out receive_give data
        receive_give = data.pop('receive_give')
        # pop out beneficiaries data
        beneficiaries = data.pop('beneficiaries')
        # create transaction instance
        serializer = self.serializer_class(data=data, context={'request': request})
        instance = Report.objects.filter(
            station=request.data['initiator']).order_by('-date_created').first()
        if request.data['category'] == SALES or request.data['category'] == CROSS_CURRENCY:
            profit = calc_profit_for_sales(receive_give)
            instance.profit += profit
            serializer.initial_data['profit'] = profit
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            # use the transaction instance to create receive_give and beneficiaries
            create_beneficiary_receiving_and_giving(receive_give=receive_give, transaction=instance, beneficiaries=beneficiaries)
            # instantiate TransactionHandler with instance
            transaction_handler = TransactionHandler(instance)
            # handle the created receive_give
            transaction_handler.handle_receive_give()
            # calculate general ledger
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    def partial_update(self, request, *args, **kwargs):
        """This partial update firstly reverses the effects of the transaction to be updated 
            using TransactionHandler.reverse_transaction then creates them again with updated values.
        Args:
            request (PATCH): transaction data should be sent along with the beneficiaries and receive_give data 
            just like creating a transaction.

        Returns:
            serializer.data: updated transaction data
        """
            # get the instance to be updated
        instance = self.queryset.get(receipt_number=request.data['receipt_number'])
        
        # instantiate TransactionHandler with instance
        transaction_handler = TransactionHandler(instance=instance)
        # reverse effects of transation
        transaction_handler.reverse_transaction()
        
        # update transaction instance
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            updated_instance = serializer.save()
            create_beneficiary_receiving_and_giving(receive_give=request.data['receive_give'], transaction=updated_instance, beneficiaries=request.data['beneficiaries'])
            transaction_handler = TransactionHandler(updated_instance)
            transaction_handler.handle_receive_give()
            data = calculation_for_general_ledger()
            data.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """deletes a transaction but firsts reverses the effects of the transaction

        Args:
            request (DELETE): transactions ID

        Returns:
            message: deletion succesfull
        """
        try:
            # get instance to be deleted
            instance = self.queryset.get(pk=kwargs.get("pk"))
            transaction_handler = TransactionHandler(instance=instance)
            # reverse transaction effects
            transaction_handler.reverse_transaction()
            # delete all beneficiaries associated wit the transaction
            instance.beneficiaries.all().delete()
            # delete the transaction
            self.perform_destroy(instance)
            # calculate general ledger
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
        """lists all reports based on the pagination settings

        Args:
            request (GET): just send a GET request to /reports/

        Returns:
            reports: list of all reports
        """
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # create new report
    def create(self, request, *args, **kwargs):
        """creates a new report with the closing balance of the last report created based on the station,
        i also should find a way to seperate frontdesk1 and frontdesk2
        if also check if you have created a report the current day or not

        Args:
            request (POST): _description_

        Returns:
            serializer: created report data
        """
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
        """retrieves report and all associated parameter including money in, money out, opening and closing balance

        Args:
            request (GET): report id required

        Returns:
            json: all parameters of the requested report
        """
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