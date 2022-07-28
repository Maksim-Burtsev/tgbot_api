from django.contrib import admin

from habr.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass