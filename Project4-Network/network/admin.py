from django.contrib import admin
from .models import Post, Likes, Following, User

# Register your models here.
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Following)
admin.site.register(User)
