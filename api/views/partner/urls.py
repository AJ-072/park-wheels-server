from rest_framework.routers import DefaultRouter
from . import BookingView

router = DefaultRouter()
router.register(r'bookings', BookingView, basename="Bookings")

urlpatterns = router.urls
