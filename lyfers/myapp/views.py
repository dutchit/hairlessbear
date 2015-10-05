from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, ProviderProfile, Jobs, Contract
from myapp.serializers import UserProfileSerializer, RegisterSerializer, ProviderProfileSerializer, JobsSerializer, ContractSerializer
import json

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

@api_view(['GET', 'POST'])
def jobs_list(request, format=None):
    """
    List all Jobs, or create a new Job.

    POST PARAMETERS
    data = {
        "userID": ID number,
        "category": "A Category",
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

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def categories_list(request, format=None):
    """
    Retrieve all Categories

    Path /api/jobs/categories/

    """

    try:
        categories = Jobs.objects.all().values_list('category').distinct()
        list_categories = []

        for elem in categories:
            list_categories.append(str(elem[0]))
        
        return Response(list_categories)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)


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
        user_jobs = Jobs.objects.filter(userID=pk).values('id', 'category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
        print (user_jobs)
        return Response(list(user_jobs))

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
        serializer = Jobs.objects.filter(id=job_number).values('id', 'category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
        return Response(serializer)

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

    return Response(status=status.HTTP_400_BAD_REQUEST)
