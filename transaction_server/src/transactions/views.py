from django.shortcuts import render
import redis, os, json
from time import time
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

redis_instance = redis.StrictRedis(charset="utf-8", decode_responses=True, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

class TransactionView(APIView):
    def get(self, request):
        keys = redis_instance.keys()
        values = []
        keys.sort()
        for key in keys:
            value = redis_instance.hgetall(key)
            values.append(value)
        return Response(values, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        # hash_key = timestamp + server_number
        hash_key = str(data["transactionNum"])
        redis_instance.sadd(hash_key, json.dumps(data))
        return Response(status=status.HTTP_200_OK)
