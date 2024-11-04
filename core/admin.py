from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model

# Register your models here.

CustomUser=get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_display=('email','name','is_active','is_staff')
    list_filter=('is_active','is_staff')
    search_fields=('email','name')


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)