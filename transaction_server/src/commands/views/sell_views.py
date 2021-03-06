from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Stock, Quote, PendingSell
from ..transactionsLogger import log_account_transaction, log_error_event
from rest_framework import status
from ..quoteHandler import get_quote
from time import time

class SellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        dollarAmount = request.data.get("amount")
        transactionNum = int(request.data.get("transactionNum"))

        try:
            dollarAmount = float(dollarAmount)
        except ValueError:
            # Log error event to transaction
            log_error_event(transactionNum, "SELL", userId, "Invalid parameter type.")
            return Response("Invalid parameter type.", status=status.HTTP_412_PRECONDITION_FAILED)


        # Find stock account
        try:
            stockAccount = Stock.objects.get(userId=userId, stockSymbol=stockSymbol)
        except Stock.DoesNotExist:
            # Log error event to transaction
            log_error_event(transactionNum, "SELL", userId, "You don't have this stock.")
            return Response("You don't have this stock.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Calculate number of stocks to sell
        stockPrice = get_quote(userId, stockSymbol, transactionNum, False)
        shares = dollarAmount/stockPrice
        
        # Check that the user has enough stocks to continue with sell
        if stockAccount.shares < shares:
            # Log error event to transaction
            log_error_event(transactionNum, "SELL", userId, "You don't have enough shares.")
            return Response("You don't have enough shares.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Record pending sell
        pendingSell = PendingSell(
            userId=userId,
            stockSymbol=stockSymbol,
            timestamp=int(time())*1000,
            dollarAmount=dollarAmount,
            shares=shares
        )
        pendingSell.save()
        
        return Response(status=status.HTTP_200_OK)


class CommitSellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        transactionNum = int(request.data.get("transactionNum"))

        # Find most recent pending sell from within the last 60 seconds, if one exists
        pendingSell = PendingSell.objects.filter(
            userId=userId,
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()


        if pendingSell is None:
            # Log error event to transaction
            log_error_event(transactionNum, "COMMIT_SELL", userId, "You don't have a sell to commit.")
            return Response("There is no sell to commit.", status=status.HTTP_412_PRECONDITION_FAILED)

        stockSymbol = pendingSell.stockSymbol
        dollarAmount = pendingSell.dollarAmount
        shares = pendingSell.shares

        # Find user account
        try:
            userAccount = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            log_error_event(transactionNum, "COMMIT_SELL", userId, "Account does not exist.")
            return Response("Account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find stock account
        try:
            stockAccount = Stock.objects.get(userId=userId, stockSymbol=stockSymbol)
        except Stock.DoesNotExist:
            # Log error event to transaction
            log_error_event(transactionNum, "COMMIT_SELL", userId, "You don't have any stock.")
            return Response("You don't have any stock.", status=status.HTTP_412_PRECONDITION_FAILED)
        
        if stockAccount.shares < shares:
            # Log error event to transaction
            log_error_event(transactionNum, "COMMIT_SELL", userId, "You don't have enough stocks.")
            return Response("You don't have enough stocks.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Increment user balance amount
        userAccount.balance += dollarAmount
        userAccount.save()

        # Remove stock shares from stock account
        stockAccount.shares -= shares
        stockAccount.save()

        # Log account transaction
        log_account_transaction(transactionNum, 'remove', userId, dollarAmount)

        # Remove pending sell
        pendingSell.delete()

        return Response(status=status.HTTP_200_OK)
        
        
class CancelSellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        transactionNum = int(request.data.get("transactionNum"))

        # Find most recent pending sell from within the last 60 seconds, if one exists
        pendingSell = PendingSell.objects.filter(
            userId=userId,
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()

        if pendingSell is None:
            # Log error event to transaction
            log_error_event(transactionNum, "CANCEL_SELL", userId, "You don't have a recent sell to cancel.")
            return Response("You don't have a recent sell to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Remove pending sell
        pendingSell.delete()
            
        return Response(status=status.HTTP_200_OK)
