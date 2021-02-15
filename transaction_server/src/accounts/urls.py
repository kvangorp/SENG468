from django.urls import path
from .views import AccountDetailView, AccountListView

urlpatterns = [
    path('accounts/<int:pk>/', AccountDetailView.as_view()),
    path('accounts/', AccountListView.as_view())
]