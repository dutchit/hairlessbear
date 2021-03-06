from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, Jobs, Contract, Application
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
        "upperBound": 0,
        "status": "A status"
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
        user_jobs = Jobs.objects.filter(userID=pk).values('id', 'title','category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound', 'status')
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
        user_jobs = Jobs.objects.filter(userID=pk, date__gte=today).values('id', 'title','category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound', 'status')
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
        user_jobs = Jobs.objects.filter(userID=pk, date__lt=today).values('id', 'title','category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound', 'status')
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
        "upperBound": 0,
        "status": "Active, Contract, Deleted, or Expired"
    }
    """

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Jobs.objects.filter(id=job_number).values('id', 'category','userID', 'description', 'location', 'date', 'duration', 'timeUnit', 'price', 'lowerBound', 'upperBound', 'status', 'title')
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
        job.status = "Deleted"
        job.save()
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
        "status": "Incomplete or Completed",
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
def poster_contracts(request, pk, format=None):
    """
    Retrieve Job Poster's Current Contracts.

    Path: /api/jobs/contracts/poster/USER_ID_NUMBER
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Contract.objects.filter(job_posterID=pk).values('id', 'applicationID','jobID','status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating', 'date')
        for current_contract in user_jobs:
            job = Jobs.objects.filter(id=current_contract['jobID']).values('title')
            print ("Poster Current Contracts")
            current_contract['job_title'] = job[0]['title']

        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def applicant_contracts(request, pk, format=None):
    """
    Retrieve Job Applicant's Current Contracts.
    
    Path: /api/jobs/contracts/applicant/USER_ID_NUMBER
    """
    today = date.today()

    try:
        userprofile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        error_response = "USER does not exist."
        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        user_jobs = Contract.objects.filter(job_applicantID=pk).values('id', 'applicationID','jobID','status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating', 'date')
        for current_contract in user_jobs:
            job = Jobs.objects.filter(id=current_contract['jobID']).values('title')
            print ("Applicant Current Contracts")
            current_contract['job_title'] = job[0]['title']
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
        for prev_contract in user_jobs:
            job = Jobs.objects.filter(id=prev_contract['jobID']).values('title')
            print ("Poster Previous Contracts")
            prev_contract['job_title'] = job[0]['title']
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
        for prev_contract in user_jobs:
            job = Jobs.objects.filter(id=prev_contract['jobID']).values('title')
            print ("Applicant Previous Contracts")
            prev_contract['job_title'] = job[0]['title']
        return Response(list(user_jobs))

    error_response = "GET method needed."
    Response(data=error_response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def contract_detail(request, contract_number, format=None):
    """
    Add or Update a Contract.

    Path: /api/jobs/contracts/CONTRACT_NUMBER

    PUT PARAMETERS
    data = {
        "id": Contract ID,
        "applicationID": Application ID,
        "jobID": Job ID,
        "status": "Incomplete, Completed, or Terminated",
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
        for user_contract in contract:
            try:
                job = Jobs.objects.filter(id=user_contract['jobID']).values('title')
            except:
                error_response = "Job does not exist."
                return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)    
            user_contract['job_title'] = job[0]['title']
        return Response(contract)

    elif request.method == 'PUT':
        serializer = ContractSerializer(contract, data=request.data)

        if serializer.is_valid():
            serializer.save()
            update_rating(request, contract)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contract = Contract.objects.get(id=contract_number)
        contract.status = "Terminated"
        contract.save()
        job = Jobs.objects.get(id=contract.jobID.id)
        job.status = "Active"
        job.save()
        application = Application.objects.get(id=contract.applicationID.id)
        application.status = "Terminated"
        application.save()
        message_response = "Contract: " + str(contract.id) + " has been terminated."
        return Response(data=message_response, status=status.HTTP_200_OK)

    error_response = "Method: " + request.method + " is wrong."
    return Response(data= error_response, status=status.HTTP_400_BAD_REQUEST)

def update_rating(request, contract):
    print("update_rating called")
    rating = 0
    poster = UserProfile.objects.get(id=contract.job_posterID.id)
    applicant = UserProfile.objects.get(id=contract.job_applicantID.id)
  
    print ("Calulating Employer Rating")
    poster_contracts = Contract.objects.filter(job_posterID=poster.id).values('job_poster_rating')
    print (poster_contracts)
    for contract in poster_contracts:
        rating = rating + contract['job_poster_rating']

    poster.employer_rating = rating/len(poster_contracts)
    poster.save()
    
    print ("Calulating Applicant Rating")
    rating = 0
    applicant_contracts = Contract.objects.filter(job_applicantID=applicant.id).values('job_applicant_rating')
    for contract in applicant_contracts:
        rating = rating + contract['job_applicant_rating']

    applicant.employee_rating = rating/len(applicant_contracts)
    applicant.save()
