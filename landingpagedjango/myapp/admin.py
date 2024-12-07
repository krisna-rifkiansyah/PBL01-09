from django.contrib import admin
from .models import Post, LogEntry

@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "image", "date_posted", "user"]

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'key', 'txt', 'session', 'ipaddr', 'app', 'time')
    list_filter = ('key', 'session', 'app', 'time')
    search_fields = ('txt', 'session', 'ipaddr')