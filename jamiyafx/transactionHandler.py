from jamiyafx.models.models2 import *
from jamiyafx.models.models1 import *
from jamiyafx.models.variables import *
from jamiyafx.utils import update_closing_and_account_bal
from datetime import date

class TransactionHandler:
    def __init__(self, instance) -> None:
        self.receive_give = instance.receive_give.all()
        self.instance = instance

        self.report = Report.objects.get(
            station=instance.initiator, date_created=instance.date_created
        )
        self.money_in = MoneyIn.objects.get(report=self.report)
        self.money_out = MoneyOut.objects.get(report=self.report)
        
    def handle_receive_give(self):
        for obj in self.receive_give:
            
            if obj.status == RECEIVING:
            
                # report balance
                setattr(
                    self.report.currencies,
                    obj.currency.lower(),
                    getattr(self.report.currencies, obj.currency.lower(), 0)
                    + obj.cash,
                )
                
                # money in
                setattr(
                    self.money_in.currencies,
                    obj.currency.lower(),
                    getattr(self.money_in.currencies, obj.currency.lower(), 0)
                    + obj.cash,
                )
                
                
                try:
                    receiving_account = Account.objects.get(
                        account_name=obj.account_name, bank_name=obj.bank_name)
                    # receiving account
                    setattr(
                        receiving_account.currencies,
                        obj.currency.lower(),
                        getattr(receiving_account.currencies,
                        obj.currency.lower())
                        + obj.transfer,
                    )
                    receiving_account.currencies.save()
                except Account.DoesNotExist:
                    pass
                self.report.currencies.save()
                self.money_in.currencies.save()
                update_closing_and_account_bal(report=self.report)
        
            elif obj.status == GIVING :
                setattr(
                self.report.currencies,
                obj.currency.lower(),
                getattr(self.report.currencies, obj.currency.lower(), 0)
                - obj.cash,
            )
            
                # money out
                setattr(
                    self.money_out.currencies,
                    obj.currency.lower(),
                    getattr(self.money_out.currencies, obj.currency.lower(), 0)
                    + obj.cash,
                )
                
                try:
                    giving_account = Account.objects.get(
                    account_name=obj.account_name, bank_name=obj.bank_name)
                    # giving account
                    setattr(
                        giving_account.currencies,
                        obj.currency.lower(),
                        getattr(giving_account.currencies,
                                obj.currency.lower())
                        - obj.transfer,
                    )
                    giving_account.currencies.save()
                except Account.DoesNotExist:
                    pass
                self.report.currencies.save()
                self.money_out.currencies.save()
                update_closing_and_account_bal(report=self.report)
                
                
                
    def reverse_transaction(self):
        print("reversed transaction successfully")
        for obj in self.receive_give:
            
            if obj.status == RECEIVING:
            
                # report balance
                setattr(
                    self.report.currencies,
                    obj.currency.lower(),
                    getattr(self.report.currencies, obj.currency.lower(), 0)
                    - obj.cash,
                )
                
                # money in
                setattr(
                    self.money_in.currencies,
                    obj.currency.lower(),
                    getattr(self.money_in.currencies, obj.currency.lower(), 0)
                    - obj.cash,
                )
                
                
                try:
                    receiving_account = Account.objects.get(
                        account_name=obj.account_name, bank_name=obj.bank_name)
                    # receiving account
                    setattr(
                        receiving_account.currencies,
                        obj.currency.lower(),
                        getattr(receiving_account.currencies,
                        obj.currency.lower())
                        - obj.transfer,
                    )
                    receiving_account.currencies.save()
                except Account.DoesNotExist:
                    pass
                self.report.currencies.save()
                self.money_in.currencies.save()
                update_closing_and_account_bal(report=self.report)
                
            
            elif obj.status == GIVING :
                setattr(
                    self.report.currencies,
                    obj.currency.lower(),
                    getattr(self.report.currencies, obj.currency.lower(), 0)
                    + obj.cash,
                )
                
                # money out
                setattr(
                    self.money_out.currencies,
                    obj.currency.lower(),
                    getattr(self.money_out.currencies, obj.currency.lower(), 0)
                    + obj.cash,
                )
                
                try:
                    giving_account = Account.objects.get(
                    account_name=obj.account_name, bank_name=obj.bank_name)
                    # giving account
                    setattr(
                        giving_account.currencies,
                        obj.currency.lower(),
                        getattr(giving_account.currencies,
                                obj.currency.lower())
                        + obj.transfer,
                    )
                    giving_account.currencies.save()
                except Account.DoesNotExist:
                    pass
                self.report.currencies.save()
                self.money_out.currencies.save()
                update_closing_and_account_bal(report=self.report)
        print('trying to delete receive_give and beneficiaries')
        self.instance.receive_give.all().delete()
        self.instance.beneficiaries.all().delete()
        print("deleted receive_give and beneficiaries")
        
        
            