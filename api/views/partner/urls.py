from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import BookingView, PartnerViewSet, ParkingLotViewSet, NotificationsViewSet, BookViewSet, SlotViewSet
from .review_viewset import ReviewViewSet
from .template_viewset import TemplateViewSet

partner_router = DefaultRouter()
partner_router.register(r'template', TemplateViewSet, basename='templates')
partner_router.register(r'bookings', BookingView, basename="Bookings")
partner_router.register(r'user', PartnerViewSet, basename="partner")
partner_router.register(r'lots', ParkingLotViewSet, basename="lots")
partner_router.register(r'notifications', NotificationsViewSet, basename="History")
parking_lot_router = NestedDefaultRouter(partner_router, r'lots', lookup="parking_lot")
parking_lot_router.register(r'book', BookViewSet, basename="Book")
parking_lot_router.register(r'slots', SlotViewSet, basename="slots")
parking_lot_router.register(r'reviews', ReviewViewSet, basename="feedback")
urlpatterns = partner_router.urls + parking_lot_router.urls
