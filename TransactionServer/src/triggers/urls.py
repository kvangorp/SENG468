from django.urls import path
from .views import TriggerListView

urlpatterns = [
    path('triggers/', TriggerListView.as_view())
]