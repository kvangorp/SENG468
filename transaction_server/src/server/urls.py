from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('accounts.urls')),
    path('api/', include('quotes.urls')),
    path('api/', include('stocks.urls')),
    path('api/', include('triggers.urls')),
    path('api/', include('transactions.urls')),
]
