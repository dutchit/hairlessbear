from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, ProviderProfile, Jobs
from myapp.serializers import UserProfileSerializer, RegisterSerializer, ProviderProfileSerializer, JobsSerializer


# Django Queryset Functions
# Multiple filters
# Table.objects.filter(param1="", param2="")

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
        userprofile = UserProfile.objects.all()
        serializer = RegisterSerializer(userprofile, many=True)
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
            username = request.data["username"]
            user = UserProfile.objects.get(username=username)
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

@api_view(['GET', 'POST'])
def jobs_list(request, format=None):
    """
    List all Jobs, or create a new Job.

    POST PARAMETERS
    data = {
        "userID": ID number,
        "description": "A description",
        "location": "A location",
        "date": "2015-09-28",
        "duration": 0,
        "timeUnit": "",
        "price": "",
        "lowerBound": 0,
        "upperBound": 0
    }
    """
    if request.method == 'GET':
        jobs = Jobs.objects.all()
        serializer = JobsSerializer(jobs, many=True)
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
            serializer = JobsSerializer(data=request.data)
        except:
            print ("Data is wrong compared to Jobs Serializer.")
            content = "Data is wrong compared to Jobs Profile Serializer."
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_jobs_list(request, pk, format=None):
    """
    Retrieve User's Jobs.

    Path: /api/jobs/USER_ID_NUMBER
    """
    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
    if request.method == 'GET':
        serializer = Jobs.objects.filter(userID=pk).values('id', 'categories','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
        return Response(list(serializer))

    Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE','PUT'])
def user_job_detail(request, pk, job_number, format=None):
    """
    Add, Delete, or Update a User's Job.

    Path: /api/jobs/USER_ID_NUMBER/JOB_NUMBER

    PUT PARAMETERS
    data = {
        "userID": ID number,
        "description": "A description",
        "location": "A location",
        "date": "2015-09-28",
        "duration": 0,
        "timeUnit": "",
        "price": "",
        "lowerBound": 0,
        "upperBound": 0
    }
    """

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Jobs.objects.filter(id=job_number).values('id', 'categories','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
        return Response(list(serializer))

    elif request.method == 'PUT':
        try:
            jobs = Jobs.objects.get(id=request.data["id"])
        except:
            return Response(data="id is missing",status=status.HTTP_400_BAD_REQUEST)

        serializer = JobsSerializer(jobs, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job = Jobs.objects.get(id=job_number)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)