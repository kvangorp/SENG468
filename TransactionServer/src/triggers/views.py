from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import TriggerSerializer
from .models import Trigger
from stocks.models import Stock

class TriggerListView(generics.GenericAPIView):
    serializer_class = TriggerSerializer
    queryset = Trigger.objects.all()

    # Handle set sell commands
    def post(self, request):

        # Make sure request can be serialized
        serializer = TriggerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check that the user has enough of the specified stock to sell
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        sharesToSell = int(request.data.get("shares"))

        stockAccount = Stock.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol
        ).first()
        
        if stockAccount.shares < sharesToSell:
            return Response("You don't have enough stocks.", status=status.HTTP_412_PRECONDITION_FAILED)

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

    
