from django.db import models

class Bot(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, help_text="You agree or make a statement on the post")
    is_active = models.BooleanField(default=True, help_text="Whether the bot is currently active.")
    personality = models.TextField(blank=True, help_text="None")

    def __str__(self):
        return self.name
