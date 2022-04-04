from typing import Any, Dict
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "authenticated": self.is_authenticated,
        }


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="PostUser")
    content = models.TextField()
    edited = models.DateTimeField(auto_now=True)

    def serialize(self) -> Dict[str, Any]:
        return {
            "user": self.user.username,
            "content": self.content,
            "edited": self.edited,
        }

    def __str__(self) -> str:
        return f"{self.user}-({self.pk})"


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LiskesUsesr")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="LikedPost")


class Fallowing(models.Model):
    fallower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Follower"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="FallowingUser"
    )
