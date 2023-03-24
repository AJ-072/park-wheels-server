from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ParkingLot, User, Slot, Booking

# Register your models here.
admin.site.register(ParkingLot)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(User, UserAdmin)
