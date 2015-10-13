from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, ProviderProfile, Jobs, Contract, Preference
from myapp.serializers import UserProfileSerializer, RegisterSerializer, ProviderProfileSerializer, JobsSerializer, ContractSerializer, PreferenceSerializer
import json

# Django Queryset Functions
# Multiple filters
# Table.objects.filter(param1="", param2="")

@api_view(['GET', 'POST'])
def contract_list(request, format=None):
    """
    List all Contracts, or create a new Contract.

    POST PARAMETERS
    data = {
        "applicationID": "Application ID number",
        "jobID": "Job ID number",
        "status": "A status",
        "job_posterID": "Job Poster ID number",
        "job_poster_rating": "Job Poster Rating",
        "job_applicantID": "Job Applicant ID number",
        "job_applicant_rating": "Job Applicant Rating",
        "payment": "Payment ID number",
    }
    """
    if request.method == 'GET':
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print ("Data: " + str(request.data))

        try:
            userID = request.data["userID"]
            user = UserProfile.objects.get(id=job_posterID)
        except:
            print ("Username is not in the system.")
            content = "Username is not in the system."
            Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = ContractSerializer(data=request.data)
        except:
            print ("Data is wrong compared to Jobs Serializer.")
            content = "Data is wrong compared to Jobs Profile Serializer."
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def preferences_list(request, format=None):
    """
    List all Preferences, or create a new Preference.

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

