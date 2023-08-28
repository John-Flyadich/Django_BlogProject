from django.contrib import admin
from .models import User, Group, Post


class YourModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'create_date', 'description', 'slug') 
    list_filter = ('author', 'title')  
    search_fields = ('author', 'title')  
    ordering = ('author',) 

admin.site.register(Group, YourModelAdmin)
admin.site.register(Post)