from django.db import models
from datetime import date

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
        return "(" + str(self.id) + ") "+ str(self.username)

class ProviderProfile(models.Model):
    userID = models.ForeignKey(UserProfile)
    profileTitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return  "(" + str(self.id) + ")" + " User ID: " + str(self.userID) + " , Title: " + str(self.profileTitle)

class Jobs(models.Model):
    userID = models.ForeignKey(UserProfile)
    category = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=date.today, blank=True)
    duration = models.IntegerField(blank=True, default=0)
    timeUnit = models.CharField(max_length=200, blank=True)
    price = models.CharField(max_length=5, blank=True)
    lowerBound = models.IntegerField(blank=True, default=0)
    upperBound = models.IntegerField(blank=True, default=0)
    status = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return "(" + str(self.id) + ") "+ "Title: " + str(self.title) + " - UserID: " + str(self.userID)

class Application(models.Model):
    jobID = models.ForeignKey(Jobs)
    posterID = models.ForeignKey(UserProfile, related_name='application_posterID')
    applicantID = models.ForeignKey(UserProfile, related_name='applicantID_applicantID')
    providerprofileID = models.ForeignKey(ProviderProfile)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return "(App ID: " + str(self.id) + ")" + " Job ID: "+ str(self.jobID) + " " + str(self.jobID.title)+ ", Poster ID: " + str(self.posterID) + ", Applicant ID: " + str(self.applicantID) + ", Provider Profile ID: " + str(self.providerprofileID)

class Contract(models.Model):
    applicationID = models.ForeignKey(Application)
    jobID = models.ForeignKey(Jobs)
    status = models.CharField(max_length=20, blank=True)
    job_posterID = models.ForeignKey(UserProfile, related_name='contract_posterID')
    job_poster_rating = models.IntegerField(blank=True, default=0)
    job_applicantID = models.ForeignKey(UserProfile, related_name='contract_applicantID')
    job_applicant_rating = models.IntegerField(blank=True, default=0)
    payment = models.ForeignKey('Payment', null=False)

class Payment(models.Model):
    contractID = models.ForeignKey(Contract, related_name='payment_contractID')
    employerID = models.ForeignKey(UserProfile, related_name='payment_employer')
    employeeID = models.ForeignKey(UserProfile, related_name='payment_employee')
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today, blank=True)

class Preference(models.Model):
    userID = models.ForeignKey(UserProfile)
    category_preference = models.CharField(max_length=200, blank=True)