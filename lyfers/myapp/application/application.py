from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, Application, ProviderProfile, Jobs, UserProfile
from myapp.serializers import ApplicationSerializer, ContractSerializer, JobsSerializer
from datetime import date
import json

@api_view(['GET', 'POST'])
def application_list(request, format=None):
    """
    List all Application, or create a Application.

    Path /api/jobs/applications

    POST PARAMETERS
    data = {
        "jobID": Job ID number,
        "application_posterID": Application Poster ID number,
        "applicantID": Applicant ID number,
        "providerprofileID": Provider Profile ID Number,
        "price": A price,
        "status": "Submited/Choosen/Declined"
    }
    """
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print ("Data: " + str(request.data))

        try:
            application_posterID = request.data["application_posterID"]
            user = UserProfile.objects.get(id=application_posterID)
        except:
            print ("Poster ID is not in the system.")
            content = "Poster ID is not in the system."
            return Response(data=content, status=status.HTTP_400_BAD_REQUEST)

        try:
            applicantID = request.data["applicantID"]
            user = UserProfile.objects.get(id=applicantID)
        except:
            print ("Appicant ID is not in the system.")
            content = "Applicant ID is not in the system."
            return Response(data=content, status=status.HTTP_400_BAD_REQUEST)

        try:
            providerprofileID = request.data["providerprofileID"]
            user = ProviderProfile.objects.get(id=providerprofileID)
        except:
            print ("Provider Profile ID is not in the system.")
            content = "Provider Profile ID is not in the system."
            return Response(data=content, status=status.HTTP_400_BAD_REQUEST)

        try:
            application = Application.objects.get(applicantID=applicantID, jobID=request.data["jobID"])
        except:      
            print("Application does not exist.")  
            try:
                serializer = ApplicationSerializer(data=request.data)
            except:
                print ("Data is wrong compared to Application Serializer.")
                content = "Data is wrong compared to Application Serializer."
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            print ("New serializer data:", serializer.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            print ("Request Data")
            print (request.data)
            serializer = ApplicationSerializer(application, data=request.data)
        except:
            error_response = "ApplicationSerializer does not match."
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            print ("Serializer data:", serializer.data)
            print ("Serializer Valid.")
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            error_response = "Serializer is not valid."
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def application_detail(request, application_number, format=None):
    """
    Retrieve or Modify an existing Application.

    Path: /api/jobs/applications/APPLICATION_NUMBER

    POST PARAMETERS
    data = {
        "jobID": Job ID number,
        "application_posterID": Application Poster ID number,
        "applicantID": Applicant ID number,
        "providerprofileID": Provider Profile ID Number,
        "price": A price,
        "status": "Submited/Choosen"
    }
    """
    try:
        application = Application.objects.get(id=application_number)
    except:
        error_response = "Application does not exist."
        return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicationSerializer(application, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def job_applicant_list(request, job_number, format=None):
    """
    Retrieve Applicants for a Specific Job.

    Path: /api/jobs/JOB_NUMBER/applicants
    """

    if request.method == 'GET':
        job_applicants = Application.objects.filter(jobID=job_number).values('id','jobID','application_posterID','applicantID','providerprofileID', 'price', 'status')
        print (job_applicants)
        return Response(list(job_applicants))

    Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def application_accepted(request, application_number, format=None):
    """
    Trigger to create a Contract.

    Path: /api/jobs/applications/APPLICATION_NUMBER/accepted
    """

    if request.method == 'POST':
        # contract.fields = ('id','applicationID', 'jobID', 'status', 'job_posterID', 'job_poster_rating', 'job_applicantID', 'job_applicant_rating')
        # application.fields = ('id','jobID', 'application_posterID', 'applicantID', 'providerprofileID', 'price', 'status')
        try:
            application = Application.objects.get(id=application_number)
            serializer = ApplicationSerializer(application)
        except:
            error_response = "Application does not exist."
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "applicationID": serializer.data["id"],
            "jobID": serializer.data["jobID"],
            "status": "Incomplete",
            "job_posterID": serializer.data["application_posterID"],
            "job_applicantID": serializer.data["applicantID"],
            "job_poster_rating": 1,
            "job_applicant_rating": 1
        }

        try:
            serializer = ContractSerializer(data=data)
        except:
            error_response = "Data does not match ContractSerializer."
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            update_job(serializer.data["jobID"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    error_response = "Request Method is not POST"
    return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

def update_job(id):
    job = Jobs.objects.get(id=id)
    job.status = "Contract"
    job.save()

@api_view(['POST'])
def application_choosen(request, application_number, format=None):
    """
    Choose an Applicant.

    Path: /api/jobs/applications/APPLICATION_NUMBER/choosen
    """

    if request.method == 'POST':
        try:
            application = Application.objects.get(id=application_number)
        except:
            error_response = "Application does not exist."
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)          
        application.status = "Choosen"
        application.save()
        user = UserProfile.objects.get(id=application.applicantID.id)
        # send_email(user)
        return Response(status=status.HTTP_200_OK)
    error_response = "Request Method is not POST"
    return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

def send_email(user):
    """
        Send email that the recipient has been choosen for the job.
    """
    title = "Lyfers: Congratulation You Have Been Choosen!"
    message = "You have been choosen for the job! Please go to www.lyfersapp.com/confirm."
    recipient = user.contactEmail
    sender = "lyfersapp@gmail.com"
    send_mail(title, message, sender, [recipient], fail_silently=False)
