from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..quoteHandler import get_quote

class QuoteView(APIView):
    def post(self, request):
        # Get request data
        userId = request.data.get("userId")
        stockSymbol = request.data.get("stockSymbol")
        transactionNum = int(request.data.get("transactionNum"))

        # Retrieve quote
        quote = get_quote(userId, stockSymbol,transactionNum,False)

        # Return quote
        data = {
            "quote": quote,
            "stockSymbol": stockSymbol
        }
        return Response(data, status=status.HTTP_200_OK)