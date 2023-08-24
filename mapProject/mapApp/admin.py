from django.contrib import admin

from .models import User
# Register your models here.

class UserAdminCustom(admin.ModelAdmin):
    list_display = ('id', "username", 'email')


admin.site.register(User, UserAdminCustom)