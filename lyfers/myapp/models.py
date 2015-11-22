from django.db import models
from datetime import date
import os

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
    employer_rating = models.IntegerField(default=0, blank=True)
    employee_rating = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return "(" + str(self.id) + ") "+ str(self.username)

class ProviderProfile(models.Model):
    userID = models.ForeignKey(UserProfile)
    profileTitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return  "(" + str(self.id) + ")" + " User ID: " + str(self.userID) + " , Title: " + str(self.profileTitle)

def image_path(instance, filename):
    filename = str(instance.userID.id) + "-" + filename
    return os.path.join('myapp/images/users', filename)

class Image(models.Model):
    userID = models.ForeignKey(ProviderProfile)
    # image = models.ImageField(upload_to='myapp/images/', blank=True, null=True)
    image = models.ImageField(upload_to=image_path, blank=True, null=True)
    def __str__(self):
        return "(" + str(self.id) + ")" + " User ID: " + str(self.userID)

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
    status = models.CharField(max_length=20, blank=True, default="Active")

    def __str__(self):
        return "(" + str(self.id) + ") "+ "Title: " + str(self.title) + " - UserID: " + str(self.userID)

class Application(models.Model):
    jobID = models.ForeignKey(Jobs)
    application_posterID = models.ForeignKey(UserProfile, related_name='application_posterID')
    applicantID = models.ForeignKey(UserProfile, related_name='applicantID_applicantID')
    providerprofileID = models.ForeignKey(ProviderProfile)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, blank=True, default="Submitted")

    def __str__(self):
        return "(App ID: " + str(self.id) + ")" + " Job ID: "+ str(self.jobID.id) + ", Title: " + str(self.jobID.title)+ ", Applicant ID: " + str(self.applicantID.id) + ", Provider Profile ID: " + str(self.providerprofileID.id) + ", Application Poster ID: " + str(self.application_posterID.id)

class Contract(models.Model):
    applicationID = models.ForeignKey(Application)
    jobID = models.ForeignKey(Jobs)
    status = models.CharField(max_length=20, blank=True)
    job_posterID = models.ForeignKey(UserProfile, related_name='contract_posterID')
    job_poster_rating = models.IntegerField(blank=True, default=0)
    job_applicantID = models.ForeignKey(UserProfile, related_name='contract_applicantID')
    job_applicant_rating = models.IntegerField(blank=True, default=0)
    date = models.DateField(default=date.today, blank=True)

    def __str__(self):
        return "(Contract ID: " + str(self.id) + ") " + "Job ID: " + str(self.jobID) + ", Job Poster ID: " + str(self.job_posterID) + ", Job Applicant ID: " + str(self.job_applicantID)

class Payment(models.Model):
    contractID = models.ForeignKey(Contract, related_name='payment_contractID')
    employerID = models.ForeignKey(UserProfile, related_name='payment_employer')
    employeeID = models.ForeignKey(UserProfile, related_name='payment_employee')
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today, blank=True)

    def __str__(self):
        return "(Payment ID: " + str(self.id) + ") " + "Contract ID: " + str(self.contractID.id) + ", Employer ID: " + str(self.employerID.id) + ", Employee ID: " + str(self.employeeID.id)

class Preference(models.Model):
    userID = models.ForeignKey(UserProfile)
    category_preference = models.CharField(max_length=200, blank=True)