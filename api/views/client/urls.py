import rest_framework.routers
from rest_framework_nested import routers
from . import ParkingLotViewSet, BookViewSet, HistoryViewSet, BookingViewSet, SlotViewSet, ClientViewSet, \
    NotificationsViewSet

client_router = routers.DefaultRouter()
client_router.register(r'parking-lots', ParkingLotViewSet, basename="parking lots")
client_router.register(r'booking', BookingViewSet, basename="Bookings")
client_router.register(r'history', HistoryViewSet, basename="History")
client_router.register(r'notifications', NotificationsViewSet, basename="History")
client_router.register(r'', ClientViewSet, basename="client")
parking_lot_router = routers.NestedDefaultRouter(client_router, r'parking-lots', lookup="parking_lot")
parking_lot_router.register(r'book', BookViewSet, basename="Book")
parking_lot_router.register(r'slots', SlotViewSet, basename="slots")

urlpatterns = client_router.urls + parking_lot_router.urls
