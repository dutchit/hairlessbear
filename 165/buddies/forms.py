from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = {'profileTitle', 'username'}
    #profileTitle = forms.CharField()
    # location = forms.CharField(widget=forms.Textarea, required=True)
    # token = forms.CharField(widget=forms.Textarea, required=True)
    #username = forms.CharField()
    # description = forms.CharField(widget=forms.Textarea)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = {'username', 'password', 'displayName'}