import json
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

from jamiyafx.models.variables import PAYABLE, RECIEVABLE, NAIRA, DOLLAR, POUND, EURO
from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.serializers import GeneralLedgerSerializer


class Dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def get_rate():
    # Find a way to get rate for the current day or use previous day rate
    pass


def update_closing_bal(report):
    closing_bal = ClosingBalance.objects.get(report=report)
    opening_bal = OpeningBalance.objects.get(report=report)
    money_in = MoneyIn.objects.get(report=report)
    money_out = MoneyOut.objects.get(report=report)

    # Get account
    account = Account.objects.get(bank_name=report.station)

    account.naira = closing_bal.naira = (
        opening_bal.naira + money_in.naira
    ) - money_out.naira
    account.dollar = closing_bal.dollar = (
        opening_bal.dollar + money_in.dollar
    ) - money_out.dollar
    account.pound = closing_bal.pound = (
        opening_bal.pound + money_in.pound
    ) - money_out.pound
    account.euro = closing_bal.euro = (
        opening_bal.euro + money_in.euro
    ) - money_out.euro
    closing_bal.save()
    account.save()


def get_customerledger_total():

    if CustomerLedger.objects.filter(status=RECIEVABLE).exists():
        recievable_totals = {
            RECIEVABLE: {
                "naira": CustomerLedger.objects.filter(status=RECIEVABLE).aggregate(
                    Sum("naira")
                )["naira__sum"],
                "dollar": CustomerLedger.objects.filter(status=RECIEVABLE).aggregate(
                    Sum("dollar")
                )["dollar__sum"],
                "pound": CustomerLedger.objects.filter(status=RECIEVABLE).aggregate(
                    Sum("pound")
                )["pound__sum"],
                "euro": CustomerLedger.objects.filter(status=RECIEVABLE).aggregate(
                    Sum("euro")
                )["euro__sum"],
            }
        }
    else:
        recievable_totals = {
            RECIEVABLE: {"naira": 0, "dollar": 0, "pound": 0, "euro": 0},
        }
    if CustomerLedger.objects.filter(status=PAYABLE).exists():
        payable_totals = {
            PAYABLE: {
                "naira": CustomerLedger.objects.filter(status=PAYABLE).aggregate(
                    Sum("naira")
                )["naira__sum"],
                "dollar": CustomerLedger.objects.filter(status=PAYABLE).aggregate(
                    Sum("dollar")
                )["dollar__sum"],
                "pound": CustomerLedger.objects.filter(status=PAYABLE).aggregate(
                    Sum("pound")
                )["pound__sum"],
                "euro": CustomerLedger.objects.filter(status=PAYABLE).aggregate(
                    Sum("euro")
                )["euro__sum"],
            },
        }

    else:
        payable_totals = {
            PAYABLE: {"naira": 0, "dollar": 0, "pound": 0, "euro": 0},
        }
    return recievable_totals, payable_totals


def calculation_for_general_ledger(data=None):
    # finding a way to calculate the report CHILLL!!!!
    (recievable_totals, payable_totals) = get_customerledger_total()
    if data is None:
        data = GeneralLedger.objects.get(date_created=datetime.date.today())
    else:
        serializer = GeneralLedgerSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data = Dotdict(serializer.data)

        # Get the total sum of all accounts for the four currencies and substract the values in payable then multiply by current rate
    naira_total = (
        Account.objects.all().aggregate(Sum("naira"))["naira__sum"]
        + payable_totals[PAYABLE]["naira"]
    ) * Rate.objects.get(date_created=datetime.date.today(), currency=NAIRA).buying

    dollar_total = (
        Account.objects.all().aggregate(Sum("dollar"))["dollar__sum"]
        + payable_totals[PAYABLE]["dollar"]
    ) * Rate.objects.get(date_created=datetime.date.today(), currency=DOLLAR).buying

    pound_total = (
        Account.objects.all().aggregate(Sum("pound"))["pound__sum"]
        + payable_totals[PAYABLE]["pound"]
    ) * Rate.objects.get(date_created=datetime.date.today(), currency=POUND).buying

    euro_total = (
        Account.objects.all().aggregate(Sum("euro"))["euro__sum"]
        + payable_totals[PAYABLE]["euro"]
    ) * Rate.objects.get(date_created=datetime.date.today(), currency=EURO).buying

    currency_total = naira_total + dollar_total + pound_total + euro_total

    data.naira = naira_total
    data.dollar = dollar_total
    data.pound = pound_total
    data.euro = euro_total
    data.currency_total = currency_total

    data.grand_total = currency_total + recievable_totals[RECIEVABLE]["naira"]
    try:
        if datetime.datetime.today().weekday() == 0:
            previous_grand_total = GeneralLedger.objects.get(
                date_created=datetime.date.today() - datetime.timedelta(days=3)
            ).grand_total
        else:
            previous_grand_total = GeneralLedger.objects.get(
                date_created=datetime.date.today() - datetime.timedelta(days=1)
            ).grand_total

        calculated_profit = Transaction.objects.filter(
            date_created=datetime.date.today()
        ).aggregate(Sum("profit"))["profit__sum"]
    except ObjectDoesNotExist:
        previous_grand_total = GeneralLedger.objects.latest("date_created").grand_total
        calculated_profit = 0.0

    data.difference = float(data.grand_total) - previous_grand_total
    data.book_profit = float(data.difference) + float(data.expense)
    data.calculated_profit = calculated_profit
    data.variance = float(data.book_profit) - float(data.calculated_profit)

    return data


class TransactionHandler:
    def __init__(self, instance) -> None:
        self.currency_recieved = instance.currency_recieved
        self.currency_given = instance.currency_given
        self.instance = instance

        self.report = Report.objects.get(
            station=instance.initiator, date_created=datetime.date.today()
        )

    def recieve_cash_give_cash(self):
        # Do cash to cash
        setattr(
            self.report,
            self.currency_recieved.lower(),
            getattr(self.report, self.currency_recieved.lower(), 0)
            + self.instance.amount_recieved,
        )
        setattr(
            self.report,
            self.currency_given.lower(),
            getattr(self.report, self.currency_given.lower(), 0)
            - self.instance.amount_given,
        )
        setattr(
            self.report,
            "profit",
            self.instance.profit + getattr(self.report, "profit", 0),
        )

        self.report.save()

        # Update money in of the report
        money_in = MoneyIn.objects.get(report=self.report)
        setattr(
            money_in,
            self.currency_recieved.lower(),
            getattr(money_in, self.currency_recieved.lower(), 0)
            + self.instance.amount_recieved,
        )
        money_in.save()

        # Update money out of the report
        money_out = MoneyOut.objects.get(report=self.report)
        setattr(
            money_out,
            self.currency_given.lower(),
            getattr(money_out, self.currency_given.lower(), 0)
            + self.instance.amount_given,
        )
        money_out.save()

        update_closing_bal(report=self.report)

    def recieve_cash_do_transfer(self):

        # Do cash to transfer
        setattr(
            self.report,
            self.currency_recieved.lower(),
            getattr(self.report, self.currency_recieved.lower(), 0)
            + self.instance.amount_recieved,
        )

        # Remove amount given from report
        setattr(
            self.report,
            self.currency_given.lower(),
            getattr(self.report, self.currency_given.lower(), 0)
            - self.instance.cash_given,
        )

        # Add profit to report
        setattr(
            self.report,
            "profit",
            self.instance.profit + getattr(self.report, "profit", 0),
        )

        self.report.save()

        # Update money in of the report
        money_in = MoneyIn.objects.get(report=self.report)
        setattr(
            money_in,
            self.currency_recieved.lower(),
            getattr(money_in, self.currency_recieved.lower(), 0)
            + self.instance.amount_recieved,
        )
        money_in.save()

        # Update money out of the report
        money_out = MoneyOut.objects.get(report=self.report)
        setattr(
            money_out,
            self.currency_given.lower(),
            getattr(money_out, self.currency_given.lower(), 0)
            + self.instance.cash_given,
        )
        money_out.save()

        # Get account used for payment
        account = Account.objects.get(bank_name=self.instance.paid_from)
        setattr(
            account,
            self.currency_given.lower(),
            getattr(account, self.currency_given.lower(), 0)
            - self.instance.amount_transfered,
        )
        account.save()
        update_closing_bal(report=self.report)

    def recieve_transfer_do_transfer(self):
        # Do transfer to transfer

        # Get account used for recieveing payment
        recieving_account = Account.objects.get(bank_name=self.instance.transfered_to)
        setattr(
            recieving_account,
            self.currency_recieved.lower(),
            getattr(recieving_account, self.currency_recieved.lower())
            + self.instance.amount_recieved,
        )
        recieving_account.save()

        # Add profit to report
        setattr(
            self.report,
            "profit",
            self.instance.profit + getattr(self.report, "profit", 0),
        )
        self.report.save()

        # Update money out of the report
        money_out = MoneyOut.objects.get(report=self.report)
        setattr(
            money_out,
            self.currency_given.lower(),
            getattr(money_out, self.currency_given.lower(), 0)
            + self.instance.cash_given,
        )
        money_out.save()

        # Get account used for payment
        account = Account.objects.get(bank_name=self.instance.paid_from)
        setattr(
            account,
            self.currency_given.lower(),
            getattr(account, self.currency_given.lower())
            - self.instance.amount_transfered,
        )
        account.save()
        update_closing_bal(report=self.report)

    def recieve_transfer_give_cash(self):
        # Get transfer and give cash

        # Get account used for recieveing payment
        recieving_account = Account.objects.get(bank_name=self.instance.transfered_to)
        setattr(
            recieving_account,
            self.currency_recieved.lower(),
            getattr(recieving_account, self.currency_recieved.lower())
            + self.instance.amount_recieved,
        )
        recieving_account.save()

        # Remove amount from report
        setattr(
            self.report,
            self.currency_given.lower(),
            getattr(self.report, self.currency_given.lower(), 0)
            - self.instance.cash_given,
        )
        self.report.save()

        # Add profit to report
        setattr(
            self.report,
            "profit",
            self.instance.profit + getattr(self.report, "profit", 0),
        )
        self.report.save()

        # Update money out of the report
        money_out = MoneyOut.objects.get(report=self.report)
        setattr(
            money_out,
            self.currency_given.lower(),
            getattr(money_out, self.currency_given.lower(), 0)
            + self.instance.cash_given,
        )
        money_out.save()

        update_closing_bal(report=self.report)
