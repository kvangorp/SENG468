from rest_framework import routers
from .views import StockListView, StockDetailView
from django.urls import include, path

urlpatterns = [
    path('stocks/', StockListView.as_view()),
    path('stocks/<str:userId>/<str:stock>/', StockDetailView.as_view())
]