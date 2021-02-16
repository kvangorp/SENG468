from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Account, Transactions
from time import time

class AddView(APIView):

    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        amount = float(request.data.get("amount"))

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
        transaction = Transactions(
            type="accountTransaction",
            timestamp=float(time()),
            server='TS',
            transactionNum=1, #TODO
            userCommand='add',
            userId=userId,
            amount=account.balance
        )
        transaction.save()
        
        return Response(status=status.HTTP_200_OK)


class DumplogView(APIView):
    def post(self, request):
        print('dumplog')


class DisplaySummaryView(APIView):
    def post(self, request):
        print('display summary')