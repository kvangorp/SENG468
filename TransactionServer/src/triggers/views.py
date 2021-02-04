from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TriggerSerializer
from .models import Trigger

class TriggerView(viewsets.ModelViewSet):
    serializer_class = TriggerSerializer
    queryset = Trigger.objects.all()
