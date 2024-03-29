from django.contrib import admin

from apps.users.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff')

admin.site.register(User, UserAdmin)
