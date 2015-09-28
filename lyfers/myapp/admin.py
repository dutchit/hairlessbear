from django.contrib import admin
from myapp.models import UserProfile, ProviderProfile, Jobs, Application, Contract, Payment

# Register your models here.
models = {UserProfile, ProviderProfile, Jobs, Application, Contract, Payment}

admin.site.register(models)