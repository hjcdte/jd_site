from django.contrib import admin
from .models import Room_Type, Room, Room_Date ,Customer, Booking_record, Money
# Register your models here.

@admin.register(Room_Type)
class Room_TypeAdmin(admin.ModelAdmin):
    list_display = ('owner','room_type')
    ordering = ('owner','room_type',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('owner','room_num','room_type')
    ordering = ('owner','room_type',)


@admin.register(Room_Date)
class Room_DateAdmin(admin.ModelAdmin):
    list_display = ('owner','roomnum','book_date','cancel_date',"is_live","is_book")
    ordering = ('owner',)

    def roomnum(self, obj):
        return obj.room.room_num

    roomnum.short_description = '房间号'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('owner','name',)
    ordering = ('owner',)


@admin.register(Booking_record)
class Booking_recordAdmin(admin.ModelAdmin):
    list_display = ('owner','customer',"room","book_date","cancel_date")
    ordering = ('owner','customer',)


@admin.register(Money)
class MoneyAdmin(admin.ModelAdmin):
    list_display = ('owner','roomnum','book_date','cancel_date',"crash")
    ordering = ('owner','book_date')

    def roomnum(self, obj):
        return obj.room.room_num

    roomnum.short_description = '房间号'

