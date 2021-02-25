from rest_framework import routers
from .views import TransactionView
from django.urls import path

urlpatterns = [
    path('transactions/', TransactionView.as_view()),
]