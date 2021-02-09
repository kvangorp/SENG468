from rest_framework import routers
from .views import StockListView, StockDetailView
from django.urls import include, path

urlpatterns = [
    path('stocks/', StockListView.as_view()),
    path('stocks/<int:pk>/', StockDetailView.as_view())
]