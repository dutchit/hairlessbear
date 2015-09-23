from django.db import models
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    profileTitle = models.CharField(max_length=202, blank=True)
    location = models.CharField(max_length=202, blank=True)
    description = models.TextField()
    token = models.CharField(max_length=220, blank=True)
    username = models.CharField(max_length=220, blank=True)
    displayName = models.CharField(max_length=200)
    first_name = models.CharField(max_length=220, blank=True)
    last_name = models.CharField(max_length=220, blank=True)
    password = models.CharField(max_length=20, blank=True)

    def __str__(self):  
        return self.username

    def saveProfile(self):
        self.save()

#Before committing, please call Ryan