from typing import Any, Dict
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self) -> Dict[str, Any]:
        return {
            "username": self.username,
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
            "id": self.pk,
        }

    def __str__(self) -> str:
        return f"{self.user}-({self.pk})"


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LikesUser")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="LikedPost")

    def __str__(self) -> str:
        return f"User {self.user} like post {self.post}"


class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Follows")
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Follower")

    def __str__(self) -> str:
        return f"user {self.follower} Following {self.follows}"
