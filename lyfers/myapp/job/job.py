from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, Jobs
from myapp.serializers import JobsSerializer
import json

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
        user_jobs = Jobs.objects.filter(userID=pk).values('id', 'title','category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
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
            jobs = Jobs.objects.get(id=job_number)
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