from django.shortcuts import render
import redis, os, json
from time import time
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserCommand, ErrorEvent

class TransactionView(APIView):
    def post(self, request):
        type = request.data.get("type")
        if type == "userCommand":
            transaction = UserCommand(
                type = type,
                timestamp = request.data.get("timestamp"),
                server = request.data.get("server"),
                transactionNum = request.data.get("transactionNum"),
                command = request.data.get("command"),
                username = request.data.get("username"),
                stockSymbol = request.data.get("stockSymbol"),
                funds = request.data.get("funds")
            )
            transaction.save()
        elif type == "errorEvent":
            transaction = ErrorEvent(
                type = type,
                timestamp = request.data.get("timestamp"),
                server = request.data.get("server"),
                transactionNum = request.data.get("transactionNum"),
                command = request.data.get("command"),
                username = request.data.get("username"),
                errorMessage = request.data.get("errorMessage")
            )
            transaction.save()
        return Response(status=status.HTTP_201_CREATED)
