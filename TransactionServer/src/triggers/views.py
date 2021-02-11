from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from .serializers import TriggerSerializer
from .models import Trigger
from stocks.models import Stock
from accounts.models import Account

class TriggerListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = TriggerSerializer
    queryset = Trigger.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId', 'stockSymbol']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
        
        if stockAccount is None or stockAccount.shares < sharesToSell:
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


class TriggerDetailView(generics.GenericAPIView):
    serializer_class = TriggerSerializer
    queryset = Trigger.objects.all()

    def get_object(self, pk):
        try:
            return Trigger.objects.get(pk=pk)
        except Trigger.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        trigger = self.get_object(pk)

        # Make sure request can be serialized
        serializer = TriggerSerializer(trigger, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save updated trigger
        serializer.save()
        return Response(serializer.data)


    def delete(self, request, pk):
        trigger = self.get_object(pk)

        # Remove reserved stock account
        reservedAccount = Stock.objects.filter(
            userId=trigger.userId,
            stockSymbol=trigger.stockSymbol,
            reserved=True
        ).first()
        reservedAccount.delete()

        # Add stocks back into regular stock account
        stockAccount = Stock.objects.filter(
            userId=trigger.userId,
            stockSymbol=trigger.stockSymbol,
            reserved=False
        ).first()
        stockAccount.shares += trigger.shares
        stockAccount.save()

        # Delete trigger
        trigger.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
