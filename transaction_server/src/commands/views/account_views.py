from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Account, Stock, Trigger
from ..transactionsLogger import log_account_transaction, log_error_event
from transactions.models import Transactions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import time
import redis, os, json
from django.conf import settings
from .database2xml import XMLgen

CACHE_TTL = getattr(settings, 'CACHE_TTL')
redis_instance = redis.StrictRedis(charset="utf-8", decode_responses=True, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

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

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        filename = request.data.get("filename")

        # Get Redis Keys, sort them, and flatten them for XMLGen
        keys_str = redis_instance.keys()
        values = []
        keys_int = list(map(int, keys_str))
        keys_int.sort()
        for key in keys_int:
            value_list = redis_instance.smembers(str(key))
            for value in value_list:
                values.append(json.loads(value))

        # Filter out at transactions not made by a specific user.
        if userId:
            values = [value for value in values if value['username'] == userId]
        
        # Create XML
        XMLgen.createDocument(filename, values)
        file = open(f'./commands/views/database2xml/{filename}.xml', 'r')
        allLines = file.read()
        file.close

        return Response(allLines, status=status.HTTP_200_OK, content_type="text/xml")


class DisplaySummaryView(APIView):

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")

        # Find user account
        try:
            userAccount = Account.objects.get(userId=userId)
        except Account.DoesNotExist:
            log_error_event(transactionNum, "DISPLAY_SUMMARY", userId, "Account does not exist.")
            return Response("Account does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        # Find stock accounts
        stocks = Stock.objects.filter(userId=userId)

        # Find triggers
        triggers = Trigger.objects.filter(userId=userId)

        # Get transaction history
        keys_str = redis_instance.keys()
        values = []
        keys_int = list(map(int, keys_str))
        keys_int.sort()
        for key in keys_int:
            value_list = redis_instance.smembers(str(key))
            for value in value_list:
                values.append(json.loads(value))

        values = [value for value in values if value['username'] == userId]

        # Return user summary
        data = {
           "userId": userId,
           "balance": userAccount.balance,
           "pending": userAccount.pending,
           "stocks": {} if not stocks else stocks.values(),
           "triggers": {} if not triggers else triggers.values(),
           "transactions": values
        }
        return Response(data,status=status.HTTP_200_OK)
