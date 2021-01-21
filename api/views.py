""" Views module of DOPIGO Challenge / Banking API """
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Account, Action, Customer
from .serializers import AccountSerializer, AccountBalanceSerializer, \
    ActionSerializer, CustomerSerializer, \
        MoneyTransferSerializer 

class AccountViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,):
    """ Creates account with an initial balance for a given customer"""
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        try:
            customer = Customer.objects.get(
                name=data['holder']
                )
        except Customer.DoesNotExist:
            return Response({'customer': 'does not exists'}, 
                status=status.HTTP_400_BAD_REQUEST)
        data['holder'] = customer.pk
        serializer = self.get_serializer(
            data=data
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    """ Lists actions of a given account, \
        takes account ID as parameter"""
    serializer_class = ActionSerializer

    def get_queryset(self):
        account_id = self.request.query_params['account_id']     
        return Action.objects.filter(
            Q(sender=account_id) |
            Q(receiver=account_id)
            )        

    def list(self, request):
        queryset = self.get_queryset() 
        if queryset.exists():
            serializer = ActionSerializer(queryset,
                many=True
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'account': 'does not exists'}, 
                status=status.HTTP_400_BAD_REQUEST)

class BalanceViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    """ Retrieves balance of a given account \
        takes account ID as parameter"""
    serializer_class = AccountBalanceSerializer

    def get_queryset(self):
        account_id = self.request.query_params['account_id']
        queryset = Account.objects.filter(pk=account_id) 
        return queryset

    def list(self, request):
        queryset = self.get_queryset() 
        if queryset.exists():
            serializer = AccountBalanceSerializer(queryset,
                many=True
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'account': 'does not exists'}, 
                status=status.HTTP_400_BAD_REQUEST)

class MoneyTransferViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    """ Creates a money transfer transaction """
    serializer_class = MoneyTransferSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        serializer = self.get_serializer(
            data=data
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






