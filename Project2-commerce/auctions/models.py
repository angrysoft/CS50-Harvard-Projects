from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category, blank=True, related_name="listings")
    image = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_bid = models.BigIntegerField(default=0)
    edited = models.DateTimeField(auto_now=True, auto_created=True, editable=False)

    def __str__(self) -> str:
        return self.title


class Bid(models.Model):
    actual_price = models.BigIntegerField(default=0, verbose_name="Bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} : {self.actual_price}"


class Comment(models.Model):
    autor = models.ForeignKey(User, on_delete=models.SET("Deleted"))
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now=True, auto_created=True, editable=False)



class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
