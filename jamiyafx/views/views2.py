from jamiyafx.models.models1 import *
from jamiyafx.models.models2 import *
from jamiyafx.serializers import *

from decouple import config
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response


# Employee Model Views


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # perform destroy of an employee instance
    def destroy(self, request, *args, **kwargs):
        # try to delete the instance if it exists and raise exception if it doesn't
        try:
            # get instance and perform destroy
            instance = self.queryset.get(pk=kwargs.get("pk"))
            self.perform_destroy(instance)
            return Response({"status": "Operation Successfull"}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OpeningBalanceViewSet(viewsets.ModelViewSet):
    queryset = OpeningBalance.objects.all()
    serializer_class = OpeningBalanceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ClosingBalanceViewSet(viewsets.ModelViewSet):
    queryset = ClosingBalance.objects.all()
    serializer_class = ClosingBalanceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ReceiveGiveViewSet(viewsets.ModelViewSet):
    queryset = ReceiveGive.objects.all()
    serializer_class = ReceiveGiveSerializer()
    permission_classes = [IsAuthenticated]
    
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer()
    permission_classes = [IsAuthenticated]
    
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    

