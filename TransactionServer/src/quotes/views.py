from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import QuoteSerializer
from .models import Quote
from rest_framework import generics, status, mixins
from rest_framework.response import Response

class QuoteView(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

    def quotes_view(request):
        serializer = QuoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data,status=status.HTTP_200_OK)

