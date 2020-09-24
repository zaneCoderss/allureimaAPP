from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'app1/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save() # save the user in db
                login(request, user) #log them in following creation of indexauth_permission_content_type_id_codename_01ab375a_uniqauth_permission
                # what the user will be taken to at login
                return redirect('userhome')
            except IntegrityError:
                return render(request, 'app1/signupuser.html', {'form':UserCreationForm(), "Error":"ERROR: That username is already registered. Please choose a different username"})

        else:
            # Tell user passwords didn't match
            return render(request, 'app1/signupuser.html', {'form':UserCreationForm(), "Error":"ERROR: Passwords did NOT match"})

def userhome(request):
    return render(request, 'app1/userhome.html')
