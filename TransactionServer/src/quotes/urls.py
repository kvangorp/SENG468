from django.urls import path
from .views import QuoteView

urlpatterns = [
    path('quotes/<str:id>/<str:sym>/', QuoteView.as_view())
]