from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('quotes.urls')),
    path('api/', include('stocks.urls')),
    path('api/', include('triggers.urls')),
]
