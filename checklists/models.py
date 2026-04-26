from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="areas")
    name = models.CharField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

class ChecklistItem(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["done", "-created_at"]

    def __str__(self):
        return self.title
