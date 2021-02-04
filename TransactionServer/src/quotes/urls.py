from rest_framework import routers
from .views import QuoteView

router = routers.DefaultRouter()
router.register('quotes', QuoteView, 'quotes')

urlpatterns = router.urls