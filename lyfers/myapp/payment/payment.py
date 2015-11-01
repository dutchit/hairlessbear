from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import UserProfile, Jobs, Contract, Payment
from myapp.serializers import JobsSerializer, ContractSerializer, PaymentSerializer
from datetime import date
import json

@api_view(['GET', 'POST'])
def payment_list(request, format=None):
    """
    List all Payments, or create a new Payment.

    Path: /api/jobs/payments

    POST PARAMETERS
    data = {
        "contractID": Contract ID Number,
        "employerID": Employer ID Number,
        "employeeID": Employee ID Number,
        "amount": An amount,
        "date" : A date (Default is today's date),
    }
    """
    if request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print ("Data: " + str(request.data))

        try:
            contract = Contract.objects.get(id=request.data["contractID"])
        except:
            print ("Contract is not in the system.")
            content = "Contract is not in the system."
            Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            employer = UserProfile.objects.get(id=request.data["employerID"])
        except:
            print ("Employer ID is not in the system.")
            content = "Employer ID is not in the system."
            Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = UserProfile.objects.get(id=request.data["employeeID"])
        except:
            print ("Employee ID is not in the system.")
            content = "Employee ID is not in the system."
            Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = PaymentSerializer(data=request.data)
        except:
            print ("Data is wrong compared to Payment Serializer.")
            content = "Data is wrong compared to Payment Serializer."
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def payment_detail(request, application_number, format=None):
    """
    Retrieve or Modify an existing Payment.

    Path: /api/jobs/payments/PAYMENT_NUMBER

    PUT PARAMETERS
    data = {
        "contractID": Contract ID Number,
        "employerID": Employer ID Number,
        "employeeID": Employee ID Number,
        "amount": An amount,
        "date" : A date (Default is today's date),
    }
    """
    try:
        payment = Payment.objects.get(id=payment_number)
    except:
        error_response = "Payment does not exist."
        return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = ApplicationSerializer(payment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicationSerializer(payment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)