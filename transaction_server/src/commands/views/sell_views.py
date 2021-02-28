from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Account, Stock, Quote
from transactions.models import Transactions
from rest_framework import status
from ..utils import get_quote
from time import time

class SellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        amount = float(request.data.get("amount"))
        transactionNum = int(request.data.get("transactionNum"))


        # Find stock account
        stockAccount = Stock.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol
        ).first()

        if not stockAccount:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='SELL',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have this stock."
            )
            transaction.save()
            return Response("You don't have this stock.", status=status.HTTP_412_PRECONDITION_FAILED)

        # TODO: review switching to checking quote cash instead
        # Calculate number of stocks to sell
        stockQuote = get_quote(id=userId, sym=stockSymbol, transactionNum=transactionNum, isSysEvent=False)
        stockPrice = stockQuote.quote
        shares = amount/stockPrice
        
        # Check that the user has enough stocks to continue with sell
        if stockAccount.shares < shares:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='SELL',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have enough shares."
            )
            transaction.save()
            return Response("You don't have enough shares.", status=status.HTTP_412_PRECONDITION_FAILED)
        
        return Response(status=status.HTTP_200_OK)


class CommitSellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        transactionNum = int(request.data.get("transactionNum"))

        # Get most recent sell transaction
        sellTransaction = self.mostRecentValidSell(userId)


        if sellTransaction is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='COMMIT_SELL',
                userId=userId,
                errorEvent="You don't have a sell to commit."
            )
            transaction.save()
            return Response("There is no sell to commit.", status=status.HTTP_412_PRECONDITION_FAILED)

        amount = sellTransaction.amount
        stockSymbol = sellTransaction.stockSymbol

        # Find user account
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()

        # Find stock account
        stockAccount = Stock.objects.filter(
            userId=userId,
            stockSymbol=stockSymbol
        ).first()

        # TODO review switching to checking quote cash instead
        # Calculate number of stocks to sell
        stockQuote = get_quote(id=userId, sym=stockSymbol, transactionNum=transactionNum, isSysEvent=False)
        stockPrice = stockQuote.quote
        shares = amount/stockPrice

        if stockAccount is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='COMMIT_SELL',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have an account."
            )
            transaction.save()
            return Response("Account doesn't exist.", status=status.HTTP_412_PRECONDITION_FAILED)
        if stockAccount.shares < shares:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='COMMIT_SELL',
                userId=userId,
                stockSymbol=stockSymbol,
                amount=amount,
                errorEvent="You don't have enough stocks."
            )
            transaction.save()
            return Response("You don't have enough stocks to sell.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Increment user balance amount
        userAccount.balance += amount
        userAccount.save()

        # Remove stock shares from stock account
        stockAccount.shares -= shares
        stockAccount.save()
        

        # Log account transaction
        transaction = Transactions(
            type="accountTransaction",
            timestamp=int(time()*1000),
            server='TS',
            transactionNum=transactionNum,
            userCommand='remove',
            userId=userId,
            amount=amount
        )
        transaction.save()

        return Response(status=status.HTTP_200_OK)


    def mostRecentValidSell(self, userId):
        # Find most recent sell in the last 60 seconds, if one exists
        recentSell = Transactions.objects.filter(
            userId=userId,
            userCommand="SELL",
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()

        # If no buy transactions exist in last 60 seconds, return None
        if recentSell is None:
            return None

        # Check for a recent cancel
        recentCancel = Transactions.objects.filter(
            userId=userId,
            userCommand="CANCEL_SELL"
        ).order_by(
            '-timestamp'
        ).first()

        # If a cancel transaction occured after the most recent buy, return None
        if recentCancel and recentCancel.timestamp > recentSell.timestamp:
            return None

        return recentSell
        
        
class CancelSellView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        transactionNum = int(request.data.get("transactionNum"))

        # Find most recent sell in the last 60 seconds, if one exists
        recentSell = Transactions.objects.filter(
            userId=userId,
            userCommand="SELL",
            timestamp__gte=int((time() - 60)*1000)
        ).order_by(
            '-timestamp'
        ).first()

        if recentSell is None:
            # Log error event to transaction
            transaction = Transactions(
                type='errorEvent',
                timestamp=int(time()*1000),
                server='TS',
                transactionNum=transactionNum,
                userCommand='CANCEL_SELL',
                userId=userId,
                errorEvent="You don't have a recent sell to cancel."
            )
            transaction.save()
            return Response("There is no recent sell to cancel.", status=status.HTTP_412_PRECONDITION_FAILED)
            
        return Response(status=status.HTTP_200_OK)
