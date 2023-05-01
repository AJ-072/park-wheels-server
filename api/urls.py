from django.urls import path, include
from .views import AuthViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'auth/(?P<user_type>(client|partner))', AuthViewSet, basename="auth")
urlpatterns = [
    path('client/', include("api.views.client.urls")),
    path('partner/', include("api.views.partner.urls")),
    path(r'', include(router.urls))
]
