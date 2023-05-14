from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ParkingLot, User, Slot, Booking, Notification, Review
from .models.parking_lot import LotImage


# Register your models here.
# admin.site.register(ParkingLot)
# admin.site.register(Slot)
# admin.site.register(User, CustomUserAdmin)


@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    list_display = ('lot', 'slot', 'booked_time', 'status')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'status', 'owner')


@admin.register(LotImage)
class LotImageAdmin(admin.ModelAdmin):
    list_display = ('lot', 'image')


@admin.register(Review)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('rating', 'comment', 'lot', 'user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'user')


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'lot')
    pass
