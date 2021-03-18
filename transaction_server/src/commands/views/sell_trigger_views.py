from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Trigger, Stock
from ..transactionsLogger import log_account_transaction, log_error_event
from rest_framework import status
from time import time

class SetSellAmountView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = request.data.get("amount")
        transactionNum = int(request.data.get("transactionNum"))

        try:
            amount = float(amount)
        except ValueError:
            # Log error event to transaction
            log_error_event(transactionNum, "SET_SELL_AMOUNT", userId, "Invalid parameter type.")
            return Response("Invalid parameter type.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find stock account
        try:
            stockAccount = Stock.objects.get(userId=userId, stockSymbol=stockSymbol)
        except Stock.DoesNotExist:
            log_error_event(transactionNum, "SET_SELL_AMOUNT", userId, "Stock account does not exist.")
            return Response("Stock account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        if stockAccount.shares < amount:
            log_error_event(transactionNum, "SET_SELL_AMOUNT", userId, "You don't have enough stocks")
            return Response("Nah ah! You don't have enough stocks.", status=status.HTTP_412_PRECONDITION_FAILED)
        
        # set aside stocks for reserved and decrement shares
        stockAccount.reserved += amount
        stockAccount.shares -= amount
        stockAccount.save()

        # Find trigger
        try:
            trigger = Trigger.objects.get(userId=userId, stockSymbol=stockSymbol, isBuy=False)
        except Trigger.DoesNotExist:
            # Create trigger
            trigger = Trigger(
                userId = userId,
                stockSymbol = stockSymbol,
                amount = amount,        #if buy, amount is dollar amount; if sell, amount is stock amount
                isBuy = False,
            )
        trigger.amount = amount
        trigger.save()

        # Log account transaction
        log_account_transaction(transactionNum, 'remove', userId, amount)

        return Response(status=status.HTTP_201_CREATED)

class SetSellTriggerView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = request.data.get("amount")
        transactionNum = int(request.data.get("transactionNum"))

        try:
            amount = float(amount)
        except ValueError:
            # Log error event to transaction
            log_error_event(transactionNum, "SET_SELL_TRIGGER", userId, "Invalid parameter type.")
            return Response("Invalid parameter type.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find trigger
        try:
            trigger = Trigger.objects.get(userId=userId, stockSymbol=stockSymbol, isBuy=False)
        except Trigger.DoesNotExist:
            # Log error event to transaction
            log_error_event(transactionNum, "SET_SELL_TRIGGER", userId, "You don't have any trigger set.")
            return Response("You don't have any trigger set.", status=status.HTTP_412_PRECONDITION_FAILED)
        trigger.triggerPoint = amount
        trigger.save()

        return Response(status=status.HTTP_200_OK)

class CancelSetSellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        transactionNum = int(request.data.get("transactionNum"))

        # Find and delete trigger
        try:
            trigger = Trigger.objects.get(userId=userId, stockSymbol=stockSymbol, isBuy=False)
        except Trigger.DoesNotExist:
            # Log error event to transaction
            log_error_event(transactionNum, "CANCEL_SET_SELL", userId, "You don't have a trigger to cancel.")
            return Response("You don't a trigger to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)


        # Find stock account and increment shares and decrement reserved
        try:
            stockAccount = Stock.objects.get(userId=userId,stockSymbol=stockSymbol)
        except Stock.DoesNotExist:
            log_error_event(transactionNum, "CANCEL_SET_SELL", userId, "Stock account does not exist.")
            return Response("Stock account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)
                
        amount = trigger.amount
        trigger.delete()
        
        stockAccount.shares += amount
        stockAccount.reserved -= amount
        stockAccount.save()

        # Log account transaction
        log_account_transaction(transactionNum, 'add', userId, amount)

        return Response(status=status.HTTP_200_OK)
