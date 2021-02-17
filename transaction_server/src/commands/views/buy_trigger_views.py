from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Trigger
from transactions.models import Transactions
from rest_framework import status
from time import time

class SetBuyAmountView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = float(request.data.get("amount"))

        # Find user account
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()

        # Check user account balance and decrement balance and increment pending 
        if userAccount.balance < amount:
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            userAccount.pending += amount
            userAccount.balance -= amount
        userAccount.save()

        # Find trigger
        trigger = Trigger.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol,
            isBuy=True
        ).first()

        # If trigger doesn't exist, create new; else, update amount
        if trigger is None:
            # Create trigger
            trigger = Trigger(
                userId = userId,
                stockSymbol = stockSymbol,
                amount = amount,
                isBuy = True,
            )
        else:
            trigger.amount = amount
        trigger.save()

        # Log account transaction
        transaction = Transactions(
            type="accountTransaction",
            timestamp=float(time()),
            server='TS',
            transactionNum=trigger.transactionNum, #TODO
            userCommand='remove',
            userId=userId,
            amount=amount
        )
        transaction.save()

        return Response(status=status.HTTP_201_CREATED)

class SetBuyTriggerView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = float(request.data.get("amount"))

        # Find trigger
        trigger = Trigger.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol,
            isBuy=True
        ).first()

        if trigger is None:
            return Response("You don't a trigger ya silly.", status=status.HTTP_412_PRECONDITION_FAILED)

        trigger.triggerPoint = amount
        trigger.save()

        return Response(status=status.HTTP_200_OK)


class CancelSetBuyView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")

        # Find and delete trigger
        trigger = Trigger.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol,
            isBuy=True
        ).first()

        if trigger is None:
            return Response("You don't a trigger to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)

        amount = trigger.amount
        trigger.delete()

        # Find user account and increment balance and decrement pending
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()
        userAccount.balance += amount
        userAccount.pending -= amount
        userAccount.save()

        # Log account transaction
        transaction = Transactions(
            type="accountTransaction",
            timestamp=float(time()),
            server='TS',
            transactionNum=trigger.transactionNum, #TODO
            userCommand='add',
            userId=userId,
            amount=amount
        )
        transaction.save()

        return Response(status=status.HTTP_200_OK)