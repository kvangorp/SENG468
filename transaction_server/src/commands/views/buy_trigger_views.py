from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Trigger
from ..transactionsLogger import log_account_transaction, log_error_event
from rest_framework import status
from time import time

class SetBuyAmountView(APIView):
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
            log_error_event(transactionNum, "SET_BUY_AMOUNT", userId, "Invalid parameter type.")
            return Response("Invalid parameter type.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find user account
        try:
            userAccount = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            log_error_event(transactionNum, "SET_BUY_AMOUNT", userId, "Account does not exist.")
            return Response("Account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Check user account balance and decrement balance and increment pending 
        if userAccount.balance < amount:
            # Log error event to transaction
            log_error_event(transactionNum, "SET_BUY_AMOUNT", userId, "You don't have enough money.")
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            userAccount.pending += amount
            userAccount.balance -= amount
        userAccount.save()

        # Find trigger
        try:
            trigger = Trigger.objects.get(userId=userId, stockSymbol=stockSymbol, isBuy=True)
        except Trigger.DoesNotExist:
            # Create trigger
            trigger = Trigger(
                userId = userId,
                stockSymbol = stockSymbol,
                amount = amount,
                isBuy = True,
            )
        # Update amount
        trigger.amount = amount
        trigger.save()

        # Log account transaction
        log_account_transaction(transactionNum, 'remove', userId, amount)

        return Response(status=status.HTTP_201_CREATED)

class SetBuyTriggerView(APIView):
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
            log_error_event(transactionNum, "SET_BUY_TRIGGER", userId, "Invalid parameter type.")
            return Response("Invalid parameter type.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find trigger
        try:
            trigger = Trigger.objects.get(userId=userId, stockSymbol=stockSymbol, isBuy=True)
        except Trigger.DoesNotExist:
            # Log error event to transaction
            log_error_event(transactionNum, "SET_BUY_TRIGGER", userId, "You don't have a trigger.")
            return Response("You don't have a trigger ya silly.", status=status.HTTP_412_PRECONDITION_FAILED)

        trigger.triggerPoint = amount
        trigger.save()

        return Response(status=status.HTTP_200_OK)


class CancelSetBuyView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        transactionNum = int(request.data.get("transactionNum"))

        # Find and delete trigger
        try:
            trigger = Trigger.objects.get(userId=userId, stockSymbol=stockSymbol, isBuy=True)
        except Trigger.DoesNotExist:
            # Log error event to transaction
            log_error_event(transactionNum, "CANCEL_SET_BUY", userId, "You don't have a trigger.")
            return Response("You don't a trigger to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)

        amount = trigger.amount
        trigger.delete()

        # Find user account and increment balance and decrement pending
        try:
            userAccount = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            log_error_event(transactionNum, "CANCEL_SET_BUY", userId, "Account does not exist.")
            return Response("Account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        userAccount.balance += amount
        userAccount.pending -= amount
        userAccount.save()

        # Log account transaction
        log_account_transaction(transactionNum, 'add', userId, amount)

        return Response(status=status.HTTP_200_OK)
