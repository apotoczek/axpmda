from django.db import models
from django.contrib.auth.models import User


class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="moods")
    mood = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mood
