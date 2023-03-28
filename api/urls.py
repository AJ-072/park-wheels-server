from django.urls import path, include, re_path
from .views import auth_view, user_view

urlpatterns = [
    path('client/', include("api.views.client.urls")),
    path('partner/', include("api.views.partner.urls")),
    path('auth/<user_type>/signin', auth_view.signin),
    path('auth/<user_type>/signup', auth_view.signup),
    re_path(r'^(?P<user_type>client|partner)/user$', user_view.UserView.as_view())
]
