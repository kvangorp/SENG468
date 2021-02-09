from django.shortcuts import render
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response
from .serializers import StockSerializer
from stocks.models import Stock
from accounts.models import Account

class StockListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId', 'stockSymbol']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request):
        # Make sure request can be serialized
        serializer = StockSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check that the user has enough of the specified stock to sell
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        sharesToSell = request.data.get("shares")

        stockAccount = Stock.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol
        ).first()
        
        if stockAccount is None or stockAccount.balance < sharesToSell:
            return Response("You don't have enough stocks to sell.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Take specified number of stocks out of user's stock account
        stockAccount.shares -= sharesToSell
        stockAccount.save()
        
        # Put specified number of stocks aside in a reserved account
        reservedStock = Stock(
            userId=userId,
            stockSymbol=stockSymbol,
            shares=sharesToSell,
            reserved=True
        )
        reservedStock.save()

        # Add the new trigger to the database
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StockDetailView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()