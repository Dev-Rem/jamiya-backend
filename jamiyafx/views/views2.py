from jamiyafx.models import *
from jamiyafx.serializers import *

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# Employee Model Views
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


# Report Model views
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


# Opening balance Model Views
class OpeningBalanceViewSet(viewsets.ModelViewSet):
    queryset = OpeningBalance.objects.all()
    serializer_class = OpeningBalanceSerializer
    permission_classes = [IsAuthenticated]


# Closing Balance Model Views
class ClosingBalanceViewSet(viewsets.ModelViewSet):
    queryset = ClosingBalance.objects.all()
    serializer_class = ClosingBalanceSerializer
    permission_classes = [IsAuthenticated]
