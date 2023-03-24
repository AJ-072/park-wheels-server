from django.urls import path, include

urlpatterns = [
    path('client/', include("api.views.client.urls"))
]
