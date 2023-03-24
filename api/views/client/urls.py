from django.urls import path
from .parking_lot_view import get_parking_lot_list,get_parking_lot

urlpatterns = [
    path('parking-lots/<ID>', get_parking_lot),
    path('parking-lots/', get_parking_lot_list),
    # path('sign-up/', )
]
