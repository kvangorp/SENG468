from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from quotes.views import QuoteView
from stocks.views import StockView
from triggers.views import TriggerView

router = routers.DefaultRouter()
router.register(r'quotes', QuoteView, 'quotes')
router.register(r'stocks', StockView, 'stocks')
router.register(r'triggers', TriggerView, 'triggers')

urlpatterns = [
    path('', include(router.urls)),
]
