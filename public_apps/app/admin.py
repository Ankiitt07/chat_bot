from django.contrib import admin
from .models import CustomUsers

# Register your models here.

class CustomUsersAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
    ]
admin.site.register(CustomUsers, CustomUsersAdmin)