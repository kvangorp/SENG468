from django.urls import path
from .views import TriggerListView, TriggerDetailView

urlpatterns = [
    path('triggers/', TriggerListView.as_view()),
    path('triggers/<int:pk>/', TriggerDetailView.as_view())
]