from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, ProviderProfile
from myapp.serializers import ProviderProfileSerializer
import json

@api_view(['GET', 'POST'])
def providerprofile_list(request, format=None):
    """
    List all Provider Profiles, or create a new Provider Profile.

    POST PARAMETERS
    data = {
    "username": "a_username", 
    "profileTitle": "A Profile Title",
    "location": "A location",
    "description": "Some Description"
    }
    """
    user = None
    if request.method == 'GET':
        providerprofile = ProviderProfile.objects.all()
        serializer = ProviderProfileSerializer(providerprofile, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print ("Data: " + str(request.data))

        try:
            userID = request.data["userID"]
            user = UserProfile.objects.get(pk=userID)
        except:
            print ("Username is not in the system.")
            content = "Username is not in the system."
            Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = ProviderProfileSerializer(data=request.data)
        except:
            print ("Data is wrong compared to Register Serializer.")
            content = "Data is wrong compared to Provider Profile Serializer."
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_providerprofile_list(request, pk, format=None):
    """
    Retrieve All User Provider Profiles.

    Path: /api/providerprofiles/USER_ID_NUMBER
    """
    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_list = ProviderProfile.objects.filter(userID=pk).values('id', 'userID', 'profileTitle', 'description', 'location')
        print (user_list)
        return Response(list(user_list))

    Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE','PUT'])
def user_providerprofile_detail(request, pk, providerprofile_number, format=None):
    """
    Add, Delete, or Update a User's Job.

    Path: /api/providerprofiles/USER_ID_NUMBER/PROVIDERPROFILE_ID_NUMBER

    PUT PARAMETERS
    data = {
        "profileTitle": "Provider Profile Title",
        "userID": USER ID Number,
        "description": "Some description",
        "id": Provider Profile ID Number,
        "location": "A location"
    }
    """

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(data="User Does Not Exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProviderProfile.objects.filter(id=providerprofile_number).values('id', 'userID', 'profileTitle', 'description', 'location')
        return Response(serializer)

    elif request.method == 'PUT':
        try:
            provider_profile = ProviderProfile.objects.get(id=providerprofile_number)
        except:
            error_response = "Cannot locate Profile Number: " + providerprofile_number
            return Response(data=error_response ,status=status.HTTP_400_BAD_REQUEST)

        serializer = ProviderProfileSerializer(provider_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        provider_profile = ProviderProfile.objects.get(id=providerprofile_number)
        provider_profile.delete()
        success_response = "Successfully deleted Provider Profile: " + providerprofile_number
        return Response(data=success_response, status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)