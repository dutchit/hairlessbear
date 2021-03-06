from rest_framework import serializers
from myapp.models import UserProfile, ProviderProfile, Jobs, Contract, Preference, Application, Payment, Image

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','username', 'profileTitle', 'description', 'contactEmail', 'displayName', 'first_name', 'last_name', 'location', 'employer_rating', 'employee_rating')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'displayName', 'contactEmail')

class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ('id', 'userID', 'profileTitle', 'description', 'location')

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ('id','category','userID', 'title', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound', 'status')

class LoginSerilizer(serializers.ModelSerializer):
    model = None

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id','applicationID', 'jobID', 'status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating')

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ('userID', 'category_preference')

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id','jobID', 'application_posterID', 'applicantID', 'providerprofileID', 'price', 'status')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'contractID', 'employerID', 'employeeID', 'amount', 'date')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'userID', 'image')