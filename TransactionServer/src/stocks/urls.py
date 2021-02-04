from rest_framework import routers
from .views import StockView

router = routers.DefaultRouter()
router.register('stocks', StockView, 'stocks')

urlpatterns = router.urls