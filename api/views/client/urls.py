import rest_framework.routers
from rest_framework_nested import routers
from . import ParkingLotViewSet, BookViewSet, HistoryViewSet, BookingViewSet, SlotViewSet

router = routers.DefaultRouter()
router.register(r'parking-lots', ParkingLotViewSet, basename="parking lots")
router.register(r'booking', BookingViewSet, basename="Bookings")
router.register(r'history', HistoryViewSet, basename="History")
parking_lot_router = routers.NestedDefaultRouter(router, r'parking-lots', lookup="parking_lot")
parking_lot_router.register(r'booking', BookViewSet, basename="Book")
parking_lot_router.register(r'slots', SlotViewSet, basename="slots")

urlpatterns = router.urls + parking_lot_router.urls
