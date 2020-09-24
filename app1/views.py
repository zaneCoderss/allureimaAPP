from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home(request):
    return render(request, 'app1/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'app1/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save() # save the user in db
                login(request, user) #log them in following creation of indexauth_permission_content_type_id_codename_01ab375a_uniqauth_permission
                return redirect('userhome')                 # what the user will be taken to at login
            except IntegrityError:
                return render(request, 'app1/signupuser.html', {'form':UserCreationForm(), "Error":"ERROR: That username is already registered. Please choose a different username"})

        else:
            # Tell user passwords didn't match
            return render(request, 'app1/signupuser.html', {'form':UserCreationForm(), "Error":"ERROR: Passwords did NOT match"})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'app1/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'app1/loginuser.html', {'form': AuthenticationForm(), 'Error':'ERROR: Username and Password did not match'})
        else:
            login(request, user) #log them in following creation of indexauth_permission_content_type_id_codename_01ab375a_uniqauth_permission
            return redirect('userhome')                 # what the user will be taken to at login


            
def userhome(request):
    return render(request, 'app1/userhome.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
