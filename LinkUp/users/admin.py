from django.contrib import admin
from .models import user
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django.db import models


class UserAdminConfig(UserAdmin):
    model = user
    search_fields = ('email', 'username', 'phone', 'full_name',)
    list_filter = ('email', 'username', 'phone', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email', 'id', 'username', 'phone', 'about',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone', 'bio', 'followers',), }),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'phone', 'password', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(user, UserAdminConfig)
