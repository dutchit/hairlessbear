from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, Jobs, Contract
from myapp.serializers import JobsSerializer, ContractSerializer
from datetime import date
import json

@api_view(['GET', 'POST'])
def jobs_list(request, format=None):
    """
    List all Jobs, or create a new Job.

    Path /api/jobs

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

@api_view(['GET', 'POST'])
def current_jobs_list(request, format=None):
    """
    List all current Jobs, or create a new Job.

    Path /api/jobs/current

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
    today = date.today()

    if request.method == 'GET':
        current_jobs = Jobs.objects.filter(date__gte=today).values('id', 'title','category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
        # serializer = JobsSerializer(jobs, many=True)
        return Response(list(current_jobs))
        # return Response(serializer.data)

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

    Path /api/jobs/categories

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

@api_view(['GET'])
def user_current_jobs_list(request, pk, format=None):
    """
    Retrieve User's Current Jobs.

    Path: /api/jobs/USER_ID_NUMBER/current
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Jobs.objects.filter(userID=pk, date__gte=today).values('id', 'title','category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
        print (user_jobs)
        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_previous_jobs_list(request, pk, format=None):
    """
    Retrieve User's Previous Jobs.

    Path: /api/jobs/USER_ID_NUMBER/previous
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Jobs.objects.filter(userID=pk, date__lt=today).values('id', 'title','category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound')
        print (user_jobs)
        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET', 'POST'])
def contract_list(request, format=None):
    """
    List all Contracts, or create a new Contract.

    Path: /api/jobs/contracts

    POST PARAMETERS
    data = {
        "applicationID": "Application ID number",
        "jobID": "Job ID number",
        "status": "A status",
        "job_posterID": "Job Poster ID number",
        "job_poster_rating": "Job Poster Rating",
        "job_applicantID": "Job Applicant ID number",
        "job_applicant_rating": "Job Applicant Rating",
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

@api_view(['GET'])
def poster_currrent_contracts(request, pk, format=None):
    """
    Retrieve Job Poster's Current Contracts.

    Path: /api/jobs/contracts/poster/USER_ID_NUMBER/current
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Contract.objects.filter(job_posterID=pk, date__gte=today).values('id', 'applicationID','jobID','status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating', 'date')
        print (user_jobs)
        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def applicant_current_contracts(request, pk, format=None):
    """
    Retrieve Job Applicant's Current Contracts.
    
    Path: /api/jobs/contracts/applicant/USER_ID_NUMBER/current
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Contract.objects.filter(job_applicantID=pk, date__gte=today).values('id', 'applicationID','jobID','status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating', 'date')
        print (user_jobs)
        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def poster_previous_contracts(request, pk, format=None):
    """
    Retrieve Job Poster's Previous Contracts.

    Path: /api/jobs/contracts/poster/USER_ID_NUMBER/current
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Contract.objects.filter(job_posterID=pk, date__lt=today).values('id', 'applicationID','jobID','status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating', 'date')
        print (user_jobs)
        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def applicant_previous_contracts(request, pk, format=None):
    """
    Retrieve Job Applicant's Previous Contracts.
    
    Path: /api/jobs/contracts/applicant/USER_ID_NUMBER/current
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Contract.objects.filter(job_applicantID=pk, date__lt=today).values('id', 'applicationID','jobID','status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating', 'date')
        print (user_jobs)
        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def contract_detail(request, contract_number, format=None):
    """
    Add or Update a Contract.

    Path: /api/contracts/CONTRACT_NUMBER

    PUT PARAMETERS
    data = {
        "id": Contract ID,
        "applicationID": Application ID,
        "jobID": Job ID,
        "status": "A status",
        "job_posterID": Job Poster ID,
        "job_poster_rating": Job Poster Rating,
        'job_applicantID': Job Applicant ID,
        'job_applicant_rating': Job Applicant Rating
    }
    """
    try:
        contract = Contract.objects.get(id=contract_number)
    except:
        error_response = "Contract Does Not Exist"
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        contract = Contract.objects.filter(id=contract_number).values('id', 'applicationID', 'jobID', 'status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating')
        return Response(contract)

    elif request.method == 'PUT':
        serializer = ContractSerializer(contract, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    error_response = "Method: " + request.method + " is wrong."
    return Response(data= error_response, status=status.HTTP_400_BAD_REQUEST)

