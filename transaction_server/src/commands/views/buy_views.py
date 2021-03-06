from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Stock, Quote, PendingBuy
from ..transactionsLogger import log_account_transaction, log_error_event
from rest_framework import status
from ..quoteHandler import get_quote
from time import time

class BuyView(APIView):
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
            log_error_event(transactionNum, "BUY", userId, "Invalid parameter type.")
            return Response("Invalid parameter type.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find user account
        try:
            userAccount = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            log_error_event(transactionNum, "BUY", userId, "Account does not exist.")
            return Response("Account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Check that the user has enough money to continue with purchase
        if userAccount.balance < amount:
            # Log error event to transaction
            log_error_event(transactionNum, "BUY", userId, "You don't have enough money.")
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Record the pending buy
        pendingBuy = PendingBuy(
            userId=userId,
            stockSymbol=stockSymbol,
            timestamp=int(time())*1000,
            dollarAmount=amount
        )
        pendingBuy.save()
        
        return Response(status=status.HTTP_200_OK)

class CommitBuyView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        transactionNum = int(request.data.get("transactionNum"))

        # Find most recent pending buy from within the last 60 seconds, if one exists
        pendingBuy = PendingBuy.objects.filter(
            userId=userId,
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()


        if pendingBuy is None:
            # Log error event to transaction
            log_error_event(transactionNum, "COMMIT_BUY", userId, "You don't have a buy to commit.")
            return Response("There is no buy to commit.", status=status.HTTP_412_PRECONDITION_FAILED)

        amount = pendingBuy.dollarAmount
        stockSymbol = pendingBuy.stockSymbol

        # Find user account
        try:
            userAccount = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            log_error_event(transactionNum, "COMMIT_BUY", userId, "Account does not exist.")
            return Response("Account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        if userAccount.balance < amount:
            # Log error event to transaction
            log_error_event(transactionNum, "COMMIT_BUY", userId, "You don't have enough money.")
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)


        # Find or create stock account
        stockAccount, created = Stock.objects.get_or_create(
            userId=userId,
            stockSymbol=stockSymbol,
            defaults={'shares':0.0}
        )

        # Calculate number of stocks to buy
        stockPrice = get_quote(userId,stockSymbol,transactionNum,False)
        shares = amount/stockPrice

        # Decrement user balance amount
        userAccount.balance -= amount
        userAccount.save()

        # Add stock shares to stock account
        stockAccount.shares += shares
        stockAccount.save()

        # Log account transaction
        log_account_transaction(transactionNum, 'remove', userId, amount)

        # Remove pending buy
        pendingBuy.delete()

        return Response(status=status.HTTP_200_OK)
        

class CancelBuyView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        transactionNum = int(request.data.get("transactionNum"))

        # Find most recent pending buy in the last 60 seconds, if one exists
        pendingBuy = PendingBuy.objects.filter(
            userId=userId,
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()

        if pendingBuy is None:
            # Log error event to transaction
            log_error_event(transactionNum, "CANCEL_BUY", userId, "You don't have a recent buy to cancel.")
            return Response("There is no recent buy to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Delete pending buy
        pendingBuy.delete()
            
        return Response(status=status.HTTP_200_OK)

    

