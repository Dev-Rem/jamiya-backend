from django.shortcuts import render

from jamiyafx.models import *
from jamiyafx.serializers import *

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response


# Employee Model Views
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# Report Model views
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


# Opening balance Model Views
class OpeningBalanceViewSet(viewsets.ModelViewSet):
    queryset = OpeningBalance.objects.all()
    serializer_class = OpeningBalanceSerializer


# Closing Balance Model Views
class ClosingBalanceViewSet(viewsets.ModelViewSet):
    queryset = ClosingBalance.objects.all()
    serializer_class = ClosingBalanceSerializer
