from django.contrib import admin
from .models import Post
# Register your models here.
class PostAdmin(admin.ModelAdmin):
     list_display = ('post_id', 'user', 'media_type', 'created_at')
     fields = ['post_id', 'user','media_type','created_at','media_url']


admin.site.register(Post,PostAdmin)
