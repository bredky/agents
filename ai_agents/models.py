from django.db import models
from django.contrib.auth.models import User

class Bot(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, help_text="You agree or make a statement on the post")
    is_active = models.BooleanField(default=True, help_text="Whether the bot is currently active.")
    personality = models.TextField(blank=True, help_text="None")

    def __str__(self):
        return self.name

class CustomBot(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(blank=True, null=True)
    likes = models.TextField(blank=True, null=True)
    dislikes = models.TextField(blank=True, null=True)
    fears = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name