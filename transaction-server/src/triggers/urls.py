from rest_framework import routers
from .views import TriggerView

router = routers.DefaultRouter()
router.register('triggers', TriggerView, 'triggers')

urlpatterns = router.urls