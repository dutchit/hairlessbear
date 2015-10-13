from django.contrib import admin
from myapp.models import UserProfile, ProviderProfile, Jobs, Application, Contract, Payment, Preference, Applicant

# Register your models here.
models = {UserProfile, ProviderProfile, Jobs, Application, Contract, Payment, Preference, Applicant}

admin.site.register(models)