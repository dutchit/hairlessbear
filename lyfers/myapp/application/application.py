from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, Application, ProviderProfile
from myapp.serializers import ApplicationSerializer
from datetime import date
import json

@api_view(['GET', 'POST'])
def application_list(request, format=None):
    """
    List all Application, or create a Application.

    Path /api/applications

    POST PARAMETERS
    data = {
        "jobID": Job ID number,
        "application_posterID": Application Poster ID number,
        "applicantID": Applicant ID number,
        "providerprofileID": Provider Profile ID Number,
        "price": A price,
        "status": "A status"
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
            Response(data=content, status=status.HTTP_400_BAD_REQUEST)

        try:
            applicantID = request.data["applicantID"]
            user = UserProfile.objects.get(id=applicantID)
        except:
            print ("Appicant ID is not in the system.")
            content = "Applicant ID is not in the system."
            Response(data=content, status=status.HTTP_400_BAD_REQUEST)

        try:
            providerprofileID = request.data["providerprofileID"]
            user = UserProfile.objects.get(id=providerprofileID)
        except:
            print ("Provider Profile ID is not in the system.")
            content = "Provider Profile ID is not in the system."
            Response(data=content, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = ApplicationSerializer(data=request.data)
        except:
            print ("Data is wrong compared to Application Serializer.")
            content = "Data is wrong compared to Application Serializer."
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        "status": "A status"
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

