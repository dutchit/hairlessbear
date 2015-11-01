from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, ProviderProfile, Jobs, Contract, Preference
from myapp.serializers import UserProfileSerializer, RegisterSerializer, ProviderProfileSerializer, JobsSerializer, ContractSerializer, PreferenceSerializer
from django.core.mail import send_mail
import json

# Django Queryset Functions
# Multiple filters
# Table.objects.filter(param1="", param2="")



@api_view(['GET', 'POST'])
def preferences_list(request, format=None):
    """
    List all Preferences, or create a new Preference.

    Path: /api/userprofiles/preferences

    POST PARAMETERS
    data = {
        "userID": "User ID number",
        "category_preference": "Category Preference",
    }
    """
    if request.method == 'GET':
        preferences = Preference.objects.all()
        serializer = PreferenceSerializer(preferences, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print ("Data: " + str(request.data))

        try:
            userID = request.data["userID"]
            user = UserProfile.objects.get(id=userID)
        except:
            print ("Username is not in the system.")
            content = "Username is not in the system."
            Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = PreferenceSerializer(data=request.data)
        except:
            print ("Data is wrong compared to Jobs Serializer.")
            content = "Data is wrong compared to Jobs Profile Serializer."
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request, format=None):
    """
        Send email to a recipient.

        Path: api/email

        POST PARAMETERS:
        data = {
            "email":"email@address.com"
        }
    """
    if request.method =='POST':
        title = "Lyfers Reset Password"
        message = "You have requested to reset your password. Please go to www.lyfersapp.com/reset_password."
        try:
            recipient = request.data["email"]
        except:        
            Response(status=status.HTTP_400_BAD_REQUEST)
        sender = "lyfersapp@gmail.com"
        send_mail(title, message, sender, [recipient], fail_silently=False)
        response = "Email sent to " + recipient
        return Response(data=response, status=status.HTTP_200_OK)    
    error_response = "Method must be POST"
    return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)