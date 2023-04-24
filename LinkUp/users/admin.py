from django.contrib import admin
from .models import user
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django.db import models



class UserAdminConfig(UserAdmin):
    model = user
    search_fields = ('email', 'username','phone','fullname',)
    list_filter = ('email', 'username','phone', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email','id','username','phone',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone',),}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','fullname', 'phone', 'password', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(user, UserAdminConfig)