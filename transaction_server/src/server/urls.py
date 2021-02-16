from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('commands.urls')),
    path('api/', include('transactions.urls'))
]
