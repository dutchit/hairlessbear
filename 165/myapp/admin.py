from django.contrib import admin
from myapp.models import UserProfile, ProviderProfile, Jobs

# Register your models here.
models = {UserProfile, ProviderProfile, Jobs}

admin.site.register(models)