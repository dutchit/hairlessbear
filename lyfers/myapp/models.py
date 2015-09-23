from django.db import models

# Create your models here.
class UserProfile(models.Model):
    profileTitle = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    token = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=200, blank=True)
    contactEmail = models.CharField(max_length=200, blank=True)
    displayName = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=20, blank=True)

    def __str__(self):  
        return self.username

class ProviderProfile(models.Model):
    username = models.ForeignKey(UserProfile)
    profileTitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "Provider Name: " + self.username.username


class Jobs(models.Model):
    username = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True)
    duration = models.IntegerField(blank=True)
    timeUnit = models.CharField(max_length=200, blank=True)
    price = models.CharField(max_length=5, blank=True)
    lowerBound = models.IntegerField(blank=True)
    upperBound = models.IntegerField(blank=True)

    def __str__(self):
        return "Jobs by: " + self.username.username