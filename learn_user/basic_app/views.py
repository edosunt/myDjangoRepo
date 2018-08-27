from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# import for login logout
from django.contrib.auth import authenticate, login, logout
# import for decorator - for checking if login session is active
from django.contrib.auth.decorators import login_required
# import for returning the html after login logout process - simple httpresponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):

    # variable to check if register process successfull, also used in register.html
    registered = False

    if request.method == 'POST':
        # grab the data from form
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileInfoForm(data=request.POST)

        # check if data is valid
        if user_form.is_valid() and user_profile_form.is_valid():
            # save the user_form data, keep it on variabel to do hashing
            user = user_form.save()
            # perform hashing
            user.set_password(user.password)
            user.save()

            # save the user profile data, commit set as false to make sure it's not created twice
            # as this is linked model
            profile = user_profile_form.save(commit = False)
            # linked with user class
            profile.user = user

            # check if user upload profile pic
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            # save the profile
            profile.save()

            registered = True
        else:
            # simply print the error from both user & user profile class
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileInfoForm()

    return render(request,'basic_app/register.html',
                {'user_form':user_form,
                    'user_profile_form':user_profile_form,
                    'registered':registered})


def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_pass')

        # perform authentication
        user = authenticate(username=user_name,password=user_password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT IS NOT ACTIVE')
        else:
            print('Someone try to login and failed')
            print('User Name: {} and Password {}'.format(user_name,user_password))
            return HttpResponse('INVALID USER ACCOUNT')

    else:
        return render(request,'basic_app/login.html',{})


# this is decorator to make sure that function below is only if user is already login
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
