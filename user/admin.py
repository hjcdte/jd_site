from django.contrib import admin
from .models import Staff

# Register your models here.
@admin.register(Staff)
class Room_TypeAdmin(admin.ModelAdmin):
    list_display = ('username','owner_username')
    ordering = ('username',)

    def owner_username(self, obj):
        return obj.owner.username

    owner_username.short_description = '员工所有人'


