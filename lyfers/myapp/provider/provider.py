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