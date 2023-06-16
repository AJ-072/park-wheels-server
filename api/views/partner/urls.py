from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import BookingView, PartnerViewSet, ParkingLotViewSet, NotificationsViewSet, BookViewSet, SlotViewSet
from .review_viewset import ReviewViewSet
from .template_viewset import TemplateViewSet

partner_router = DefaultRouter()
partner_router.register(r'template', TemplateViewSet, basename='templates')
partner_router.register(r'booking', BookingView, basename="Bookings")
partner_router.register(r'parking-lots', ParkingLotViewSet, basename="lots")
partner_router.register(r'notifications', NotificationsViewSet, basename="History")
partner_router.register(r'', PartnerViewSet, basename="partner")
parking_lot_router = NestedDefaultRouter(partner_router, r'parking-lots', lookup="parking_lot")
parking_lot_router.register(r'book', BookViewSet, basename="Book")
parking_lot_router.register(r'slots', SlotViewSet, basename="slots")
parking_lot_router.register(r'reviews', ReviewViewSet, basename="feedback")
urlpatterns = partner_router.urls + parking_lot_router.urls
