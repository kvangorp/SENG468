from rest_framework import routers
from .views import TransactionView

router = routers.DefaultRouter()
router.register('transactions', TransactionView, 'transactions')

urlpatterns = router.urls