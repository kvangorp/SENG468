from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Stock, Quote, PendingBuy
from transactions.models import Transactions
from rest_framework import status
from ..utils import get_quote
from time import time

class BuyView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = float(request.data.get("amount"))
        transactionNum = int(request.data.get("transactionNum"))

        # Find user account
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()

        # Check that the user has enough money to continue with purchase
        if userAccount.balance < amount:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='BUY',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have enough money."
            )
            transaction.save()
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Record the pending buy
        pendingBuy = PendingBuy(
            userId=userId,
            stockSymbol=stockSymbol,
            timestamp=int(time()*1000),
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
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='COMMIT_BUY',
                userId=userId,
                errorEvent="You don't have a buy to commit."
            )
            transaction.save()
            return Response("There is no buy to commit.", status=status.HTTP_412_PRECONDITION_FAILED)

        amount = pendingBuy.dollarAmount
        stockSymbol = pendingBuy.stockSymbol

        # Find user account
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()

        if userAccount is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='COMMIT_BUY',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have a user account."
            )
            transaction.save()
            return Response("Account doesn't exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        if userAccount.balance < amount:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='COMMIT_BUY',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have enough money."
            )
            transaction.save()
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)


        # Find or create stock account
        stockAccount, created = Stock.objects.get_or_create(
            userId=userId,
            stockSymbol=stockSymbol,
            defaults={'shares':0.0}
        )

        # TODO review switching to checking quote cash instead
        # Calculate number of stocks to buy
        stockQuote = get_quote(userId,stockSymbol,transactionNum,False)
        stockPrice = stockQuote.quote
        shares = amount/stockPrice

        # Decrement user balance amount
        userAccount.balance -= amount
        userAccount.save()

        # Add stock shares to stock account
        stockAccount.shares += shares
        stockAccount.save()

        # Log account transaction
        transaction = Transactions(
            type="accountTransaction",
            timestamp=int(time()*1000),
            server='TS',
            transactionNum=transactionNum, #TODO
            userCommand='remove',
            userId=userId,
            amount=amount
        )
        transaction.save()

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
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='CANCEL_BUY',
                userId=userId,
                errorEvent="You don't have a recent buy to cancel."
            )
            transaction.save()
            return Response("There is no recent buy to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Delete pending buy
        pendingBuy.delete()
            
        return Response(status=status.HTTP_200_OK)

    

