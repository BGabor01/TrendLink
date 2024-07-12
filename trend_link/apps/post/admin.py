from django.contrib import admin
from apps.post.models import Post, Comment, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
