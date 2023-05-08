from jamiyafx.models.models2 import *
from jamiyafx.models.models1 import *
from jamiyafx.utils import update_closing_and_account_bal


class TransactionHandler:
    def __init__(self, instance) -> None:
        self.receiving = instance.receiving.all()
        self.giving = instance.giving.all()
        self.instance = instance

        self.report = Report.objects.get(
            station=instance.initiator, date_created=datetime.date.today()
        )
        self.money_in = MoneyIn.objects.get(report=self.report)
        self.money_out = MoneyOut.objects.get(report=self.report)
        
    def handle_receiving(self):
        print('updating report and account with receiving')
        for receive in self.receiving:
            
            # report balance
            setattr(
                self.report.currencies,
                receive.currency_received.lower(),
                getattr(self.report.currencies, receive.currency_received.lower(), 0)
                + receive.cash_received,
            )
            
            # money in
            setattr(
                self.money_in.currencies,
                receive.currency_received.lower(),
                getattr(self.money_in.currencies, receive.currency_received.lower(), 0)
                + receive.cash_received,
            )
            
            
            try:
                receiving_account = Account.objects.get(
                    account_name=receive.receive_account_name, bank_name=receive.receive_bank_name)
                # receiving account
                setattr(
                    receiving_account.currencies,
                    receive.currency_received.lower(),
                    getattr(receiving_account.currencies,
                    receive.currency_received.lower())
                    + receive.receive_amount_transfered,
                )
                receiving_account.currencies.save()
            except Account.DoesNotExist:
                pass
        
        self.report.currencies.save()
        self.money_in.currencies.save()
        update_closing_and_account_bal(report=self.report)
        
    def handle_giving(self):
        print('updating report and account with giving')
        for give in self.giving:
            setattr(
                self.report.currencies,
                give.currency_given.lower(),
                getattr(self.report.currencies, give.currency_given.lower(), 0)
                - give.cash_given,
            )
            
            # money out
            setattr(
                self.money_out.currencies,
                give.currency_given.lower(),
                getattr(self.money_out.currencies, give.currency_given.lower(), 0)
                + give.cash_given,
            )
            
            try:
                giving_account = Account.objects.get(
                account_name=give.give_account_name, bank_name=give.give_bank_name)
                # giving account
                setattr(
                    giving_account.currencies,
                    give.currency_given.lower(),
                    getattr(giving_account.currencies,
                            give.currency_given.lower())
                    - give.give_amount_transfered,
                )
                giving_account.currencies.save()
            except Account.DoesNotExist:
                pass
            
        self.report.currencies.save()
        self.money_out.currencies.save()
        update_closing_and_account_bal(report=self.report)
    
    def reverse_transaction(self):
        
        for receive in self.receiving:
            
            # report balance
            setattr(
                self.report.currencies,
                receive.currency_received.lower(),
                getattr(self.report.currencies, receive.currency_received.lower(), 0)
                - receive.cash_received,
            )
            
            # money in
            setattr(
                self.money_in.currencies,
                receive.currency_received.lower(),
                getattr(self.money_in.currencies, receive.currency_received.lower(), 0)
                - receive.cash_received,
            )
            
            
            try:
                receiving_account = Account.objects.get(
                    account_name=receive.receive_account_name, bank_name=receive.receive_bank_name)
                # receiving account
                setattr(
                    receiving_account.currencies,
                    receive.currency_received.lower(),
                    getattr(receiving_account.currencies,
                    receive.currency_received.lower())
                    - receive.receive_amount_transfered,
                )
                receiving_account.currencies.save()
            except Account.DoesNotExist:
                pass
        
        self.report.currencies.save()
        self.money_in.currencies.save()
        update_closing_and_account_bal(report=self.report)
        
        for give in self.giving:
            setattr(
                self.report.currencies,
                give.currency_given.lower(),
                getattr(self.report.currencies, give.currency_given.lower(), 0)
                + give.cash_given,
            )
            
            # money out
            setattr(
                self.money_out.currencies,
                give.currency_given.lower(),
                getattr(self.money_out.currencies, give.currency_given.lower(), 0)
                - give.cash_given,
            )
            
            try:
                giving_account = Account.objects.get(
                account_name=give.give_account_name, bank_name=give.give_bank_name)
                # giving account
                setattr(
                    giving_account.currencies,
                    give.currency_given.lower(),
                    getattr(giving_account.currencies,
                            give.currency_given.lower())
                    + give.give_amount_transfered,
                )
                giving_account.currencies.save()
            except Account.DoesNotExist:
                pass
            
        self.report.currencies.save()
        self.money_out.currencies.save()
        update_closing_and_account_bal(report=self.report)
        
        self.receiving.delete()
        self.giving.delete()
            
    # def recieve_cash_give_cash(self):
    #     # Do cash to cash
        
        
    #     for receive in self.receiving:
    #         setattr(
    #             self.report.currencies,
    #             receive.currency_given.lower(),
    #             getattr(self.report.currencies, receive.currency_given.lower(), 0)
    #             + receive.cash_received,
    #         )
    #         # Update money in of the report
    #         setattr(
    #             money_in.currencies,
    #             self.currency_recieved.lower(),
    #             getattr(money_in.currencies, self.currency_recieved.lower(), 0)
    #             + receive.amount_recieved,
    #         )
    #     for give in self.giving:
            
    #         setattr(
    #             self.report.currencies,
    #             give.currency_given.lower(),
    #             getattr(self.report.currencies, give.currency_given.lower(), 0)
    #             - self.instance.cash_given,
    #         )
            
    #         # Update money out of the report
    #         setattr(
    #             money_out.currencies,
    #             self.currency_given.lower(),
    #             getattr(money_out.currencies, self.currency_given.lower(), 0)
    #             + self.instance.cash_given,
    #         )
    #     setattr(
    #         self.report,
    #         "profit",
    #         self.instance.profit + getattr(self.report, "profit", 0),
    #     )

        


 

    # def recieve_cash_do_transfer(self):

    #     # Do cash to transfer
    #     setattr(
    #         self.report.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(self.report.currencies, self.currency_recieved.lower(), 0)
    #         + self.instance.cash_received,
    #     )

    #     # Get account used for payment
    #     setattr(
    #         self.payment_account.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.payment_account.currencies,
    #                 self.currency_given.lower(), 0)
    #         - self.instance.give_amount_transfered,
    #     )

    #     # Add profit to report
    #     setattr(
    #         self.report,
    #         "profit",
    #         self.instance.profit + getattr(self.report, "profit", 0),
    #     )

    #     # Update money in of the report
    #     money_in = MoneyIn.objects.get(report=self.report)
    #     setattr(
    #         money_in.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(money_in.currencies, self.currency_received.lower(), 0)
    #         + self.instance.cash_received,
    #     )

    #     self.payment_account.currencies.save()
    #     self.report.currencies.save()
    #     money_in.currencies.save()
    #     update_closing_and_account_bal(report=self.report)

    # def recieve_transfer_do_transfer(self):
    #     # Get account used for recieveing payment
    #     setattr(
    #         self.receiving_account.currencies,
    #         self.currency_received.lower(),
    #         getattr(self.receiving_account.currencies,
    #                 self.currency_recieved.lower())
    #         + self.instance.receive_amount_transfered,
    #     )

    #     # Add profit to report
    #     setattr(
    #         self.report,
    #         "profit",
    #         self.instance.profit + getattr(self.report, "profit", 0),
    #     )
    #     # update paymnet account

    #     setattr(
    #         self.payment_account.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.payment_account.currencies,
    #                 self.currency_given.lower())
    #         - self.instance.give_amount_transfered,
    #     )

    #     self.receiving_account.currencies.save()
    #     self.report.currencies.save()
    #     self.payment_account.currencies.save()
    #     update_closing_and_account_bal(report=self.report)

    # def recieve_transfer_give_cash(self):

    #     # Get account used for recieveing payment
    #     setattr(
    #         self.receiving_account.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(self.receiving_account.currencies,
    #                 self.currency_recieved.lower())
    #         + self.instance.receive_amount_transfered,
    #     )

    #     # Remove amount from report
    #     setattr(
    #         self.report.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.report.currencies, self.currency_given.lower(), 0)
    #         - self.instance.cash_given,
    #     )

    #     # Add profit to report
    #     setattr(
    #         self.report,
    #         "profit",
    #         self.instance.profit + getattr(self.report, "profit", 0),
    #     )

    #     # Update money out of the report
    #     money_out = MoneyOut.objects.get(report=self.report)
    #     setattr(
    #         money_out.currencies,
    #         self.currency_given.lower(),
    #         getattr(money_out.currencies, self.currency_given.lower(), 0)
    #         + self.instance.cash_given,
    #     )
    #     self.receiving_account.currencies.save()
    #     money_out.currencies.save()
    #     self.report.currencies.save()
    #     update_closing_and_account_bal(report=self.report)

    # def receive_transfer_and_cash_give_cash(self):
    #     # receive transfer
    #     setattr(
    #         self.receiving_account.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(self.receiving_account.currencies,
    #                 self.currency_recieved.lower())
    #         + self.instance.receive_amount_transfered,
    #     )

    #     # receive cash
    #     setattr(
    #         self.report.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(self.report.currencies, self.currency_recieved.lower(), 0)
    #         + self.instance.cash_received,
    #     )

    #     setattr(
    #         self.report,
    #         "profit",
    #         self.instance.profit + getattr(self.report, "profit", 0),
    #     )

    #     money_in = MoneyIn.objects.get(report=self.report)
    #     setattr(
    #         money_in.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(money_in.currencies, self.currency_received.lower(), 0)
    #         + self.instance.cash_received,
    #     )
    #     # give cash
    #     setattr(
    #         self.report.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.report.currencies, self.currency_given.lower(), 0)
    #         - self.instance.cash_given,
    #     )

    #     money_out = MoneyOut.objects.get(report=self.report)
    #     setattr(
    #         money_out.currencies,
    #         self.currency_given.lower(),
    #         getattr(money_out.currencies, self.currency_given.lower(), 0)
    #         + self.instance.cash_given,
    #     )

    #     self.receiving_account.currencies.save()
    #     money_in.currencies.save()
    #     self.report.currencies.save()
    #     money_out.currencies.save()
    #     update_closing_and_account_bal(report=self.report)

    # def receive_cash_give_transfer_and_cash(self):

    #     # recceive cash
    #     setattr(
    #         self.report.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(self.report.currencies, self.currency_recieved.lower(), 0)
    #         + self.instance.cash_received,
    #     )

    #     setattr(
    #         self.report,
    #         "profit",
    #         self.instance.profit + getattr(self.report, "profit", 0),
    #     )

    #     #
    #     money_in = MoneyIn.objects.get(report=self.report)
    #     setattr(
    #         money_in.currencies,
    #         self.currency_recieved.lower(),
    #         getattr(money_in.currencies, self.currency_received.lower(), 0)
    #         + self.instance.cash_received,
    #     )

    #     # give transfer
    #     setattr(
    #         self.payment_account.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.payment_account.currencies,
    #                 self.currency_given.lower())
    #         - self.instance.give_amount_transfered,
    #     )

    #     # give cash
    #     setattr(
    #         self.report.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.report.currencies, self.currency_given.lower(), 0)
    #         - self.instance.cash_given,
    #     )

    #     money_out = MoneyOut.objects.get(report=self.report)
    #     setattr(
    #         money_out.currencies,
    #         self.currency_given.lower(),
    #         getattr(money_out.currencies, self.currency_given.lower(), 0)
    #         + self.instance.cash_given,
    #     )

    #     money_out.currencies.save()
    #     money_in.currencies.save()
    #     self.payment_account.currencies.save()
    #     self.report.currencies.save()
    #     update_closing_and_account_bal(report=self.report)

    # def receive_transfer_give_cash_and_transfer(self):
    #     # receive transfer
    #     setattr(
    #         self.receiving_account,
    #         self.currency_recieved.lower(),
    #         getattr(self.receiving_account, self.currency_recieved.lower())
    #         + self.instance.receive_amount_transfered,
    #     )

    #     # give cash
    #     setattr(
    #         self.report.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.report.currencies, self.currency_given.lower(), 0)
    #         - self.instance.cash_given,
    #     )

    #     money_out = MoneyOut.objects.get(report=self.report)
    #     setattr(
    #         money_out.currencies,
    #         self.currency_given.lower(),
    #         getattr(money_out.currencies, self.currency_given.lower(), 0)
    #         + self.instance.cash_given,
    #     )
    #     # give transfer
    #     setattr(
    #         self.payment_account.currencies,
    #         self.currency_given.lower(),
    #         getattr(self.payment_account.currencies,
    #                 self.currency_given.lower())
    #         - self.instance.give_amount_transfered,
    #     )
    #     setattr(
    #         self.report,
    #         "profit",
    #         self.instance.profit + getattr(self.report, "profit", 0),
    #     )

    #     self.receiving_account.currencies.save()
    #     self.report.currencies.save()
    #     money_out.currencies.save()
    #     self.payment_account.currencies.save()
    #     update_closing_and_account_bal(report=self.report)
