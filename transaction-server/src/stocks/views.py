from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StockSerializer
from .models import Stock

class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
