from jamiyafx.serializers import GeneralLedgerSerializer
from jamiyafx.models.models2 import *
from jamiyafx.models.models1 import *
from jamiyafx.serializers import *
from jamiyafx.models.variables import PAYABLE, RECIEVABLE, NAIRA, DOLLAR, POUND, EURO
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from datetime import date
class Dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# function to update the closing balance of a report


def update_closing_and_account_bal(report):
    # get report variables for the report parsed
    closing_bal = ClosingBalance.objects.get(report=report)
    opening_bal = OpeningBalance.objects.get(report=report)
    money_in = MoneyIn.objects.get(report=report)
    money_out = MoneyOut.objects.get(report=report)

    # Get the account for the report parsed
    account = Account.objects.get(bank_name=report.station)

    # update account values witht the closing balance calculated with variables for diffrent currencies
    account.currencies.naira = closing_bal.currencies.naira = (
        opening_bal.currencies.naira + money_in.currencies.naira
    ) - money_out.currencies.naira

    account.currencies.dollar = closing_bal.currencies.dollar = (
        opening_bal.currencies.dollar + money_in.currencies.dollar
    ) - money_out.currencies.dollar

    account.currencies.pound = closing_bal.currencies.pound = (
        opening_bal.currencies.pound + money_in.currencies.pound
    ) - money_out.currencies.pound

    account.currencies.euro = closing_bal.currencies.euro = (
        opening_bal.currencies.euro + money_in.currencies.euro
    ) - money_out.currencies.euro

    closing_bal.currencies.save()
    account.currencies.save()


# function to get customer ledger totals
def get_currency_total(objects):
    totals = {"naira": 0, "dollar": 0, "pound": 0, "euro": 0}

    if objects.count() >= 1:
        for ledger in objects:
            curencies = Currency.objects.get(id=ledger.currencies.id)
            totals['naira'] += curencies.naira
            totals['dollar'] += curencies.dollar
            totals['pound'] += curencies.pound
            totals['euro'] += curencies.euro

    else:
        pass

    return totals


# function to calculate general ledger
def calculation_for_general_ledger(data=None):

    factory = APIRequestFactory()
    request = factory.get('/')

    recievable_totals = get_currency_total(
        CustomerLedger.objects.filter(status=RECIEVABLE))

    payable_totals = get_currency_total(
        CustomerLedger.objects.filter(status=PAYABLE))

    account_totals = get_currency_total(Account.objects.all())

    # check if data is parsed or not
    if data is None:
        data = GeneralLedger.objects.get(date_created=date.today())
        general_ledger_currencies = Currency.objects.get(id=data.currencies.id)

    else:
        general_ledger_currencies = Currency.objects.create(
            **data['currencies'])
        data['currencies'] = general_ledger_currencies.id
        serializer = GeneralLedgerSerializer(
            data=data, context={"request": Request(request)})
        if serializer.is_valid(raise_exception=True):
            data = Dotdict(serializer.data)
    # Get the total sum of all accounts for the four currencies and substract the values in payable then multiply by current rate
    naira_total = (
        account_totals['naira']
        + payable_totals["naira"]
    ) * Rate.objects.get(currency=NAIRA).buying

    dollar_total = (
        account_totals['dollar']
        + payable_totals["dollar"]
    ) * Rate.objects.get(currency=DOLLAR).buying

    pound_total = (
        account_totals['pound']
        + payable_totals["pound"]
    ) * Rate.objects.get(currency=POUND).buying

    euro_total = (
        account_totals['euro']
        + payable_totals["euro"]
    ) * Rate.objects.get(currency=EURO).buying

    # calculate curency total
    currency_total = naira_total + dollar_total + pound_total + euro_total
    # assign values to the data
    general_ledger_currencies.naira = naira_total
    general_ledger_currencies.dollar = dollar_total
    general_ledger_currencies.pound = pound_total
    general_ledger_currencies.euro = euro_total
    data.currency_total = currency_total
    general_ledger_currencies.save()
    # calculate for grand total
    data.grand_total = currency_total + recievable_totals["naira"]
    # try to get previous general ledger grand total and assign to prervious total of current day
    try:
        queryset = GeneralLedger.objects.order_by(
            '-date_created')
        if queryset[0].date_created == date.today():
            previous_grand_total = queryset[1].grand_total
        else:
            previous_grand_total = queryset[0].grand_total

    except ObjectDoesNotExist:
        previous_grand_total = data.grand_total

    # get the total sum of all profit calculated from reports created at present day
    calculated_profit = Report.objects.filter(
        date_created=date.today()
    ).aggregate(Sum("profit"))["profit__sum"]

    # assign previous total
    data.previous_total = previous_grand_total
    # assign the difference of previous total and present grand total
    data.difference = float(data.grand_total) - float(data.previous_total)
    # calculate book profit from difference and expense
    data.book_profit = float(data.difference) + float(data.expense)
    if calculated_profit:
        data.calculated_profit = calculated_profit
    else:
        data.calculated_profit = 0
    data.variance = float(data.book_profit) - float(data.calculated_profit)

    return data



def create_beneficiary_receiving_and_giving(receive_give,transaction, beneficiaries = None):
    print(transaction)
    for i in receive_give:
        try:
            i.pop('transaction')
        except:
            pass
        obj = ReceiveGive.objects.create(transaction=transaction, **i)
        obj.save()
    if beneficiaries == None:
        pass
    else:
        for j in beneficiaries:
            beneficiary = Beneficiary.objects.create(transaction=transaction, **j)
            beneficiary.save()

def calc_profit_for_cross_currency(receive_give):
    profit=0
    receive_total = 0
    give_total = 0
    # iterate through receive_give list
    for i in receive_give:
        
        if i['status'] == RECEIVING:
            # multiply cash by cash rate and transfer by transfer rate
            # then add to receive total so we can keep track of customer balance
            if i['cash_rate' ]> 0 and i['cash']>0:
                cash = i['cash'] * i['cash_rate']
            if i['transfer_rate' ]> 0 and i['transfer']>0:
                transfer = i['transfer'] * i['transfer_rate']
            receive_total += cash + transfer
            
        if i['status'] == GIVING:
            # get account ledger buying rate based on currency
            rate = Rate.objects.get(currency=i['currency']).buying
            
            if i['cash_rate' ]> 0 and i['cash']>0:
                profit += (i["cash_rate"] - rate) * (i['cash'])
                cash = i['cash'] * i['cash_rate']
            if i['transfer_rate' ]> 0 and i['transfer']>0:
                profit += (i["transfer_rate"] - rate) * (i['transfer'])
                transfer = i['transfer'] * i['transfer_rate']
            give_total += cash + transfer
            
    return profit
    
def calc_profit_for_sales(receive_give):
    profit = 0
    for i in receive_give:
        if i['status'] == GIVING:
            # get account ledger buying rate based on currency
            rate = Rate.objects.get(currency=i['currency']).buying
            
            if i['cash_rate' ]> 0 and i['cash']>0:
                profit += (i["cash_rate"] - rate) * i['cash']
            if i['transfer_rate' ]> 0 and i['transfer']>0:
                profit += (i["transfer_rate"] - rate) * (i['transfer'])
                
    return profit


def calc_for_purchase(receive_give):
    
    receive_total = 0
    give_total = 0
    for i in receive_give:
        if i['status'] == RECEIVING:
            if i['cash_rate' ]> 0 and i['cash']>0:
                cash = i['cash'] * i['cash_rate']
            if i['transfer_rate' ]> 0 and i['transfer']>0:
                transfer = i['transfer'] * i['transfer_rate']
            receive_total += cash + transfer
        if i['status'] == GIVING:
            if i['cash_rate' ]> 0 and i['cash']>0:
                cash = i['cash'] * i['cash_rate']
            if i['transfer_rate' ]> 0 and i['transfer']>0:
                transfer = i['transfer'] * i['transfer_rate']
            give_total += cash + transfer

    return receive_total==give_total