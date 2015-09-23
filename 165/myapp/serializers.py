from rest_framework import serializers
from myapp.models import UserProfile, ProviderProfile, Jobs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','username', 'profileTitle', 'description', 'contactEmail', 'displayName', 'first_name', 'last_name', 'location')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'displayName', 'contactEmail')

class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ('id', 'username', 'profileTitle', 'description', 'location')

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ('username', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')

class LoginSerilizer(serializers.ModelSerializer):
    model = None