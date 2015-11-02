from django.contrib import admin
from myapp.models import UserProfile, ProviderProfile, Jobs, Application, Contract, Payment, Preference, Image

# Register your models here.
models = {UserProfile, ProviderProfile, Jobs, Application, Contract, Payment, Preference, Image}

admin.site.register(models)