from jamiyafx.serializers import GeneralLedgerSerializer
from jamiyafx.models.models2 import *
from jamiyafx.models.models1 import *
from jamiyafx.serializers import *
from jamiyafx.models.variables import PAYABLE, RECIEVABLE, NGN, USD, GBP, EUR
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
    account.currencies.ngn = report.currencies.ngn = closing_bal.currencies.ngn = (
        opening_bal.currencies.ngn + money_in.currencies.ngn
    ) - money_out.currencies.ngn

    account.currencies.usd =  report.currencies.usd = closing_bal.currencies.usd = (
        opening_bal.currencies.usd + money_in.currencies.usd
    ) - money_out.currencies.usd

    account.currencies.gbp =  report.currencies.gbp = closing_bal.currencies.gbp = (
        opening_bal.currencies.gbp + money_in.currencies.gbp
    ) - money_out.currencies.gbp

    account.currencies.eur =  report.currencies.eur = closing_bal.currencies.eur = (
        opening_bal.currencies.eur + money_in.currencies.eur
    ) - money_out.currencies.eur

    report.currencies.save()
    closing_bal.currencies.save()
    account.currencies.save()


# function to get customer ledger totals
def get_currency_total(objects):
    totals = {"ngn": 0, "usd": 0, "gbp": 0, "eur": 0}

    if objects.count() >= 1:
        for ledger in objects:
            curencies = Currency.objects.get(id=ledger.currencies.id)
            totals['ngn'] += curencies.ngn
            totals['usd'] += curencies.usd
            totals['gbp'] += curencies.gbp
            totals['eur'] += curencies.eur

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
    ngn_total = (
        account_totals['ngn']
        + payable_totals["ngn"]
    ) * Rate.objects.get(currency=NGN).buying

    usd_total = (
        account_totals['usd']
        + payable_totals["usd"]
    ) * Rate.objects.get(currency=USD).buying

    gbp_total = (
        account_totals['gbp']
        + payable_totals["gbp"]
    ) * Rate.objects.get(currency=GBP).buying

    eur_total = (
        account_totals['eur']
        + payable_totals["eur"]
    ) * Rate.objects.get(currency=EUR).buying

    # calculate curency total
    currency_total = ngn_total + usd_total + gbp_total + eur_total
    # assign values to the data
    general_ledger_currencies.ngn = ngn_total
    general_ledger_currencies.usd = usd_total
    general_ledger_currencies.gbp = gbp_total
    general_ledger_currencies.eur = eur_total
    data.currency_total = currency_total
    general_ledger_currencies.save()
    # calculate for grand total
    data.grand_total = currency_total + recievable_totals["ngn"]
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



def create_beneficiary_receiving_and_giving(receive_give,transaction, beneficiaries ):
    for i in receive_give:
        try:
            i.pop('transaction')
        except:
            pass
        obj = ReceiveGive.objects.create(transaction=transaction, **i)
        obj.save()

    for j in beneficiaries:
        try:
            j.pop('transaction')
        except:
            pass
        obj = Beneficiary.objects.create(transaction=transaction, **j)
        obj.save()

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