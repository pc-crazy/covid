from django.contrib import admin
from corona.models import User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', "country", "first_name", "last_name",)


admin.site.register(User, UserAdmin)
