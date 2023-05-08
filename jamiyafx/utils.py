from jamiyafx.serializers import GeneralLedgerSerializer
from jamiyafx.models.models2 import *
from jamiyafx.models.models1 import *
from jamiyafx.serializers import *
from jamiyafx.models.variables import PAYABLE, RECIEVABLE, NAIRA, DOLLAR, POUND, EURO
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


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
        data = GeneralLedger.objects.get(date_created=datetime.today())
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
        if queryset[0].date_created == datetime.today():
            previous_grand_total = queryset[1].grand_total
        else:
            previous_grand_total = queryset[0].grand_total

    except ObjectDoesNotExist:
        previous_grand_total = data.grand_total

    # get the total sum of all profit calculated from reports created at present day
    calculated_profit = Report.objects.filter(
        date_created=datetime.today()
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



def create_receiving_and_giving(receiving, giving, transaction):
    for i in receiving:
            receiving = Receiving.objects.create(transaction=transaction, **i)
            receiving.save()
    for j in giving:
        giving = Giving.objects.create(transaction=transaction, **j)
        giving.save()

def get_profit_for_sales(data):
    profit = 0
    for i in data:
        rate = Rate.objects.get(currency=i['currency_given']).buying
        
        profit += (i["selling_rate"] - rate) * (i['cash_given']+i['give_amount_transfered'])

    return profit

