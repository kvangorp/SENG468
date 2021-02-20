from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Trigger, Stock
from transactions.models import Transactions
from rest_framework import status
from time import time

class SetSellAmountView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = float(request.data.get("amount"))

        # Find stock account
        stockAccount = Stock.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol
        ).first()
        lastTransaction = Transactions.objects.last()

        # return if user doesn't have any or enough stocks
        if stockAccount is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=lastTransaction.transactionNum,
                userCommand='SET_SELL_AMOUNT',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have any stock."
            )
            transaction.save()
            return Response("You don't have any stock.", status=status.HTTP_412_PRECONDITION_FAILED)
        if stockAccount.shares < amount:
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=lastTransaction.transactionNum,
                userCommand='SET_SELL_AMOUNT',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have enough stocks."
            )
            transaction.save()
            return Response("Nah ah! You don't have enough stocks.", status=status.HTTP_412_PRECONDITION_FAILED)
        
        # set aside stocks for reserved and decrement shares
        stockAccount.reserved += amount
        stockAccount.shares -= amount
        stockAccount.save()

        # Find trigger
        trigger = Trigger.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol,
            isBuy=False
        ).first()

        # If trigger doesn't exist, create new; else, update amount
        if trigger is None:
            # Create trigger
            trigger = Trigger(
                userId = userId,
                stockSymbol = stockSymbol,
                amount = amount,        #if buy, amount is dollar amount; if sell, amount is stock amount
                isBuy = False,
            )
        else:
            trigger.amount = amount
        trigger.save()

        # Log account transaction
        transaction = Transactions(
            type="accountTransaction",
            timestamp=int(time()*1000),
            server='TS',
            transactionNum=lastTransaction.transactionNum, 
            userCommand='remove',
            userId=userId,
            amount=amount
        )
        transaction.save()

        return Response(status=status.HTTP_201_CREATED)

class SetSellTriggerView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = float(request.data.get("amount"))

        # Find trigger
        trigger = Trigger.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol,
            isBuy=False
        ).first()

        lastTransaction = Transactions.objects.last()

        # If trigger doesn't exist, create new; else, update amount
        if trigger is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=lastTransaction.transactionNum,
                userCommand='SET_SELL_TRIGGER',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have any trigger set."
            )
            transaction.save()
            return Response("You don't have any trigger set.", status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            trigger.triggerPoint = amount
        trigger.save()

        return Response(status=status.HTTP_200_OK)

class CancelSetSellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")

        # Find and delete trigger
        trigger = Trigger.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol,
            isBuy=False
        ).first()

        lastTransaction = Transactions.objects.last()

        if trigger is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=lastTransaction.transactionNum,
                userCommand='CANCEL_SET_SELL',
                userId=userId,
                stockSymbol=stockSymbol,
                errorEvent="You don't have a trigger to cancel."
            )
            transaction.save()
            return Response("You don't a trigger to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)
        amount = trigger.amount
        trigger.delete()

        # Find stock account and increment shares and decrement reserved
        stockAccount = Stock.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol,
        ).first()
        stockAccount.shares += amount
        stockAccount.reserved -= amount
        stockAccount.save()

        lastTransaction = Transactions.objects.last()
        # Log account transaction
        transaction = Transactions(
            type="accountTransaction",
            timestamp=int(time()*1000),
            server='TS',
            transactionNum=lastTransaction.transactionNum, 
            userCommand='add',
            userId=userId,
            amount=amount
        )
        transaction.save()

        return Response(status=status.HTTP_200_OK)
