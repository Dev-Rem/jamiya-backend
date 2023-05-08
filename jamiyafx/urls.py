from rest_framework import routers
from jamiyafx.views.views1 import *
from jamiyafx.views.views2 import *

router = routers.SimpleRouter()

router.register(r"accounts", AccountViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"reports", ReportViewSet)
router.register(r"moneyins", MoneyInViewSet)
router.register(r"moneyouts", MoneyOutViewSet)
router.register(r"openingbalances", OpeningBalanceViewSet)
router.register(r"closingbalances", ClosingBalanceViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"rates", RateViewSet)
router.register(r"customerledgers", CustomerLedgerViewSet)
router.register(r'generalledger', GeneralLedgerViewSet)
router.register(r'receiving', ReceiveGiveViewSet)

urlpatterns = router.urls