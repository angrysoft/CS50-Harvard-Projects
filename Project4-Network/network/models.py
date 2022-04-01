from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    text = models.TextField(verbose_name="New Post")
    added = models.DateTimeField(auto_now=True, editable=False)
