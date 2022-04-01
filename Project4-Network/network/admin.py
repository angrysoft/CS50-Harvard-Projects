from django.contrib import admin
from .models import Post, Likes, Fallowing, User

# Register your models here.
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Fallowing)
admin.site.register(User)
