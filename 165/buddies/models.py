from django.db import models
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    profileTitle = models.TextField()
    location = models.TextField()
    description = models.TextField()
    token = models.TextField()
    username = models.TextField()
    displayName = models.CharField(max_length=200)
    first_name = models.TextField()
    last_name = models.TextField()
    password = models.CharField(max_length=20, blank=True)

    def __str__(self):  
        return self.username

    def saveProfile(self):
        self.save()
