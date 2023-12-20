from django.contrib import admin
from .models import Room,RoomType,RoomReservation
#--------------------------------------------------------
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RoomReservation)
#--------------------------------------------------------