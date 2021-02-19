from django.contrib import admin
from django.urls import path, include
from commands import triggerHandler
import threading

urlpatterns = [
    path('api/', include('commands.urls')),
    path('api/', include('transactions.urls'))
]

t1 = threading.Thread(target=triggerHandler.triggerHandler, daemon=True)
t1.start()
