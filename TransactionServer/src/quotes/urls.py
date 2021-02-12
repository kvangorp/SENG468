from django.urls import path
from .views import quotes_view

urlpatterns = [
    path('quotes/', quotes_view.as_view()),
    path('quotes/<string:quotesymbol>/', quotes_view.as_view())
]