from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    pass
