from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Account, Stock, Trigger
from ..transactionsLogger import log_account_transaction
from transactions.models import Transactions
from time import time
import redis, os
from django.conf import settings

redis_instance = redis.StrictRedis(charset="utf-8", decode_responses=True, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

class AddView(APIView):

    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        amount = float(request.data.get("amount"))
        transactionNum = int(request.data.get("transactionNum"))

        # Find or create user account
        account = Account.objects.filter(
            userId=userId,
        ).first()

        if account is None:
            account = Account(userId=userId)

        # Add money to account
        account.balance += amount
        account.save()

        # Log transaction
        log_account_transaction(transactionNum, 'add', userId, amount)
       
        return Response(status=status.HTTP_200_OK)


class DumplogView(APIView):
    def post(self, request):
        userId = request.data.get("userId")
        keys = redis_instance.keys()
        values = []
        keys.sort()
        for key in keys:
            value = redis_instance.hgetall(key)
            print(value)
            # print(value['username'])
            values.append(value)
        return Response(values, status=status.HTTP_200_OK)


class DisplaySummaryView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")

        # Find user account
        userAccount = Account.objects.filter(
            userId=userId,
        ).first()

        # Find stock accounts
        stocks = Stock.objects.filter(
            userId=userId
        )

        # Find triggers
        triggers = Trigger.objects.filter(
            userId=userId
        )

        # Get transaction history
        transactions= Transactions.objects.filter(
            userId=userId
        )

        # Return user summary
        data = {
            "userId": userId,
            "balance": userAccount.balance,
            "pending": userAccount.pending,
            "stocks": stocks.values(),
            "triggers": triggers.values(),
            "transactions": transactions.values()
        }
        return Response(data, status=status.HTTP_200_OK)
