from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TransactionSerializer
from .models import Transactions

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transactions.objects.all()