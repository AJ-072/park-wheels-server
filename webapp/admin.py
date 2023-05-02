from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ParkingLot, User, Slot, Booking, Notifications


# Register your models here.
# admin.site.register(ParkingLot)
# admin.site.register(Slot)
# admin.site.register(User, CustomUserAdmin)


@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'status', 'owner')


@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    pass
