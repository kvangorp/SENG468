from django.urls import path
from .views import AccountDetailView

urlpatterns = [
    path('accounts/<int:pk>/', AccountDetailView.as_view())
]