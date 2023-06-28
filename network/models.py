from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    followers = models.ManyToManyField("User", related_name="following", blank=True)
    def __str__(self):
        return f"{self.username} has {self.followers.count()} followers and is following {self.following.count()} users"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    def __str__(self):
        return f"{self.user} posted {self.content} at {self.timestamp}"
    