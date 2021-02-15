from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import QuoteSerializer
from .models import Quote
from transactions.models import Transactions
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from django.http import Http404
from .methods import quoteClient


class QuoteView(generics.GenericAPIView):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

    def get_quote(self,id,sym):
        data = quoteClient(sym,id)
        elements = data.split(',')
        print(elements)
        quoteResult = Quote(
            quote=float(elements[0]),
            stockSymbol=elements[1],
            userId=elements[2],
            timestamp=float(elements[3]),
            cryptokey=elements[4]
        )

        transaction = Transactions(
            type="quoteServer",
            timestamp=float(elements[3]),
            server='QS',
            transactionNum=1, #TODO
            price=float(elements[0]),
            stockSymbol=elements[1],
            userId=elements[2],
            quoteServerTime=float(elements[3]),
            cryptoKey=elements[4]
        )
        transaction.save()
        return quoteResult

    def get(self, request, id,sym): #return json of pk
        quote = self.get_quote(id,sym)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)

    def put(self, request, id,sym):
        quote = self.get_quote(id,sym)

        # Make sure request can be serialized
        serializer = QuoteSerializer(quote, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save updated trigger
        serializer.save()
        return Response(serializer.data)


