from django.contrib import admin
from .models import user,Item,orderlog
admin.site.register(user)
admin.site.register(Item)
admin.site.register(orderlog)