from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Notes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    notes_data = models.TextField()
    thumbnail = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
