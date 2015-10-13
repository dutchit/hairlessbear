from django.contrib import admin
from myapp.models import UserProfile, ProviderProfile, Jobs, Application, Contract, Payment, Preference

# Register your models here.
models = {UserProfile, ProviderProfile, Jobs, Application, Contract, Payment, Preference}

admin.site.register(models)