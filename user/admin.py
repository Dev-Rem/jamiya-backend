from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Customize the display fields in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'station', 'is_active')
    # Add filters and search fields if needed
    list_filter = ('station', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'station', 'first_name','last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_admin',
         'is_superuser', 'station')}
         ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)