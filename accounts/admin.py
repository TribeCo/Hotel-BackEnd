from django.contrib import admin
from .models import User,RoomComment,FoodComment,Comment
#--------------------------------------------------------
admin.site.register(User)
admin.site.register(RoomComment)
admin.site.register(FoodComment)
admin.site.register(Comment)
#--------------------------------------------------------