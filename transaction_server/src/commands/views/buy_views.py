from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Stock, Quote
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

        # Find user account
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()

        # Check that the user has enough money to continue with purchase
        if userAccount.balance < amount:
            lastTransaction = Transactions.objects.last()
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=lastTransaction.transactionNum,
                userCommand='BUY',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have enough money."
            )
            transaction.save()
            return Response("You don't have enough money.", status=status.HTTP_412_PRECONDITION_FAILED)
        
        return Response(status=status.HTTP_200_OK)

class CommitBuyView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")

        # Get most recent buy transaction
        buyTransaction = self.mostRecentValidBuy(userId)

        lastTransaction = Transactions.objects.last()

        if buyTransaction is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=lastTransaction.transactionNum,
                userCommand='COMMIT_BUY',
                userId=userId,
                errorEvent="You don't have a buy to commit."
            )
            transaction.save()
            return Response("There is no buy to commit.", status=status.HTTP_412_PRECONDITION_FAILED)

        amount = buyTransaction.amount
        stockSymbol = buyTransaction.stockSymbol

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
                transactionNum=lastTransaction.transactionNum,
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
                transactionNum=lastTransaction.transactionNum,
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
        stockQuote = get_quote(userId,stockSymbol,lastTransaction.transactionNum,False)
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
            transactionNum=lastTransaction.transactionNum, #TODO
            userCommand='remove',
            userId=userId,
            amount=amount
        )
        transaction.save()

        return Response(status=status.HTTP_200_OK)


    def mostRecentValidBuy(self, userId):
        # Find most recent buy in the last 60 seconds, if one exists
        recentBuy = Transactions.objects.filter(
            userId=userId,
            userCommand="BUY",
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()

        # If no buy transactions exist in last 60 seconds, return None
        if recentBuy is None:
            return None

        # Check for a recent cancel
        recentCancel = Transactions.objects.filter(
            userId=userId,
            userCommand="CANCEL_BUY"
        ).order_by(
            '-timestamp'
        ).first()

        # If a cancel transaction occured after the most recent buy, return None
        if recentCancel and recentCancel.timestamp > recentBuy.timestamp:
            return None

        return recentBuy
        

class CancelBuyView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")

        # Find most recent buy in the last 60 seconds, if one exists
        recentBuy = Transactions.objects.filter(
            userId=userId,
            userCommand="BUY",
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()

        if recentBuy is None:
            lastTransaction = Transactions.objects.last()
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=lastTransaction.transactionNum,
                userCommand='CANCEL_BUY',
                userId=userId,
                errorEvent="You don't have a recent buy to cancel."
            )
            transaction.save()
            return Response("There is no recent buy to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)
            
        return Response(status=status.HTTP_200_OK)

    

