from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Account, Stock, Trigger
from ..transactionsLogger import log_account_transaction, log_error_event
from transactions.models import UserCommand, QuoteServerTransaction, ErrorEvent, AccountTransaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import time
import redis, os, json
from django.conf import settings
from transactions.serializers import AccountTransactionSerializer, UserCommandSerializer, ErrorEventSerializer, QuoteServerTransactionSerializer
from django.core import serializers

# CACHE_TTL = getattr(settings, 'CACHE_TTL')

class AddView(APIView):

    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        amount = request.data.get("amount")
        transactionNum = int(request.data.get("transactionNum"))

        try:
            amount = float(amount)
        except ValueError:
            # Log error event to transaction
            log_error_event(transactionNum, "ADD", userId, "Invalid parameter type.")
            return Response("Invalid parameter type.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find or create user account
        try:
            account = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            account = Account(userId=userId)

        # Add money to account
        account.balance += amount
        account.save()

        # Log transaction
        log_account_transaction(transactionNum, 'add', userId, amount)

        # time.sleep(20)
       
        return Response(status=status.HTTP_200_OK)


class DumplogView(APIView):

    # @method_decorator(cache_page(CACHE_TTL))
    def post(self, request):
        userId = request.data.get("userId")
        if not userId:
            userCommands = UserCommandSerializer(UserCommand.objects.all(), many=True)
            accountTransactions = AccountTransactionSerializer(AccountTransaction.objects.all(), many=True)
            quoteServerTransactions = QuoteServerTransactionSerializer(QuoteServerTransaction.objects.all(), many=True)
            errorEvents = ErrorEventSerializer(ErrorEvent.objects.all(), many=True)
        else:
            userCommands = UserCommandSerializer(UserCommand.objects.filter(username=userId), many=True)
            accountTransactions = AccountTransactionSerializer(AccountTransaction.objects.filter(username=userId), many=True)
            quoteServerTransactions = QuoteServerTransactionSerializer(QuoteServerTransaction.objects.filter(username=userId), many=True)
            errorEvents = ErrorEventSerializer(ErrorEvent.objects.filter(username=userId), many=True)
        
        all_transactions = userCommands.data + accountTransactions.data + \
            quoteServerTransactions.data + errorEvents.data
        all_transactions.sort(key=lambda transaction: transaction['transactionNum'])

        return Response(all_transactions, status=status.HTTP_200_OK)


class DisplaySummaryView(APIView):

    # @method_decorator(cache_page(CACHE_TTL))
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")

        # Find user account
        try:
            userAccount = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            return Response("Account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find stock accounts
        stocks = Stock.objects.filter(userId=userId)

        # Find triggers
        triggers = Trigger.objects.filter(userId=userId)

        # Get transaction history
        #transactions= Transactions.objects.filter(userId=userId)

        # Return user summary
        data = {
           "userId": userId,
           "balance": userAccount.balance,
           "pending": userAccount.pending,
           "stocks": {} if not stocks else stocks.values(),
           "triggers": {} if not triggers else triggers.values(),
        #    "transactions": transactions.values()
        }
        return Response(data,status=status.HTTP_200_OK)
