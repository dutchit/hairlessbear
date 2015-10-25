from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, Jobs
from myapp.serializers import UserProfileSerializer, RegisterSerializer
import json

@api_view(['GET', 'POST'])
def userprofile_list(request, format=None):
    """
    List all User Profiles, or create a new User Profile.

    POST PARAMETERS
    data = {
    "username": "a_username", 
    "password": "password",
    "displayName": "Sample Display",
    "contactEmail": "Contact Email"
    }
    """
    user = None
    userprofile = None
    print ("UserProfile_list is called.")

    if request.method == 'GET':
#        userprofile = UserProfile.objects.all()
        try:
            username = request.query_params.get('username')
            password = request.query_params.get('password')
            print ("request: ",username, password)
            userprofile = UserProfile.objects.get(username=username, password=password)
        except:
            print ("username and password is not in the system.")
            return Response("Username and password are invalid.", status=status.HTTP_400_BAD_REQUEST)
        if userprofile:
            print ("found it")
            serializer = UserProfileSerializer(userprofile)
            return Response(serializer.data)

    elif request.method == 'POST':
        user = request.data["username"]

        try:
            #Getting username from POST request (request.data["username"])
            #Query the UserProfile Table using username
            user = UserProfile.objects.get(username=user)
            print ("User exists")
        except:
            print ("Username is not in the system.")
            try:
                serializer = RegisterSerializer(data=request.data)
            except:
                print ("Data is wrong compared to Register Serializer.")
                print ("Request Data: " + str(request.data))
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        if user:
            print ("User exists.")
            return Response(status=status.HTTP_409_CONFLICT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def userprofile_detail(request, pk, format=None):
    """
    Retrieve, update or delete a User Profile.

    Path: api/userprofile/USER_ID_NUMBER

    """
    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(userprofile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        userprofile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def job_list(request, pk, format=None):
    """
    Retreive all employer jobs associated with a User Profile

    Path: api/userprofile/USER_ID_NUMBER/jobs
    """

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        jobs = Jobs.objects.filter(userID=pk).values('id')
        return Response(list(jobs))

    error_response = "Method is not GET"
    return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


