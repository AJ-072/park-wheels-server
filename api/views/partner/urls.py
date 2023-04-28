from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from . import BookingView, PartnerViewSet

partner_router = DefaultRouter()
partner_router.register(r'bookings', BookingView, basename="Bookings")

urlpatterns = partner_router.urls
