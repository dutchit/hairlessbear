from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
#import django.http
#from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from .forms import UserProfileForm, RegisterForm
import json


# Create your views here.
@csrf_exempt
def addUser(request):
    print ("Adding a user")
    print ("Post info: " + str(request.POST))

    response_data = {}
    try:
        form = RegisterForm(request.POST)

    except:
        print ("Registration Issue")


    try:
        user = UserProfile.objects.get(username=request.POST.get("username"))
        if user:
            response_data = {"message": "User already exists"}
            return HttpResponseBadRequest("User exists")
    except:
        print ("User does not exist")

    if form.is_valid():
        try:
            form.save()
        except:
            print("Registration Form not Saved")

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    return HttpResponseBadRequest("Registration Form Is Not Valid")

@csrf_exempt
def addUserProfile(request):
    print ("Processing addUserProfile")
    # post_data = request.POST.get("userProfile")


    # location = models.TextField()
    # description = models.TextField()
    # token = models.TextField()

    print (str(request.method))
    print
    print (request.POST)
    #user = User.objects.get(username=request.POST.get("username"))
    #request.POST = request.POST.copy()
    #request.POST['username'] = user


    try:
        user = UserProfile.objects.get(username=request.POST.get("username"))
    except:
        print ("UserProfile issue")
    if user:
        print ("User exists")
        return render('buddies/index.html')

    form = UserProfileForm(request.POST)

    print ("Is form valid? " + str(form.is_valid()))
    if form.is_valid():
        try:
            profile = form.save(commit=False)
            print ("Temp save complete")
        except:
            print ("An error occurred during first save")
        profile.location = "No where"
        profile.description = "Test description"
        profile.token = "no token for now"
        profile.displayName = "TESTING TESTING"
        
        try:
            profile.save()
            print ("Profile has been saved.")
        except:
            print ("Profile has NOT been saved.")

    response_data = {}


    response_data['user'] = {
        "name": profile.username,
        "contactEmail": profile.username,
        "userProfile": {
            "profileTitle": profile.profileTitle,
            "location": profile.location,
            "description": profile.description
        },
        "providerProfiles": []
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def homePage(request):
    return render(request, "buddies/index.html", {}) 