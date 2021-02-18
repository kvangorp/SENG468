from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..utils import get_quote
from transactions.models import Transactions

class QuoteView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")

        # Retrieve quote
        lastTransaction = Transactions.objects.last()
        quote = get_quote(userId, stockSymbol,lastTransaction.transactionNum,False)

        # Return quote
        data = {
            "quote": quote.quote,
            "stockSymbol": quote.stockSymbol
        }
        return Response(data, status=status.HTTP_200_OK)