from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TransactionSerializer
from .models import Transactions
from django_filters.rest_framework import DjangoFilterBackend

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transactions.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId', 'userCommand']