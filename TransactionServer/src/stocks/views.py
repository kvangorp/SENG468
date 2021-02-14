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

class StockDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    # def get_quote(self,id,sym):
    #     data = quoteClient(sym,id)
    #     elements = data.split(',')
 
    #     quoteResult = Quote(
    #         quote=float(elements[0]),
    #         stockSymbol=elements[1],
    #         userId=elements[2],
    #         timestamp=float(elements[3]),
    #         cryptokey=elements[4]
    #     )
    #     return quoteResult

    # def get(self, request, id,sym): #return json of pk
    #     quote = self.get_quote(id,sym)
    #     serializer = QuoteSerializer(quote)
    #     return Response(serializer.data)
    
    def get(self,request,action,userId,stock):
        stock = Stock.objects.filter(userId=userId,stockSymbol=stock).first()
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    #TODO: add check for buy vs sell
    def put(self, request, action, userId, stock):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        shares = float(request.data.get("shares"))
        amount = float(request.data.get("amount"))

        # Find user account
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()

        if userAccount is None:
            return Response("Account doesn't exist.", status=status.HTTP_412_PRECONDITION_FAILED)
        if userAccount.balance < amount:
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find stock account
        stockAccount = Stock.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol
        ).first()

        if stockAccount is None:
            stockAccount = Stock(
                userId=userId,
                stockSymbol=stockSymbol,
                shares=0.0
            )
        if action == 'buy':
            # Decrement user balance amount
            userAccount.balance -= amount
            userAccount.save()

            # Add stock shares
            stockAccount.shares += shares
            stockAccount.save()
        else:
            # Decrement user balance amount
            userAccount.balance += amount
            userAccount.save()

            # Add stock shares
            stockAccount.shares -= shares
            stockAccount.save()

        # Make sure request can be serialized
        serializer = StockSerializer(stockAccount)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
