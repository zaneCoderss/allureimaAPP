from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required



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


@login_required
def userhome(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'app1/userhome.html', {'todos': todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'app1/completedtodos.html', {'todos': todos})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def addTodo(request):
    if request.method == 'GET':
        return render(request, 'app1/addTodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False) #creating a new to do object when someone creates a new one
            newTodo.user = request.user
            newTodo.save()
            return redirect('userhome')
        except ValueError:
            return render(request, 'app1/addtodo.html', {'Form': TodoForm(), 'error': 'Please Try Again'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'app1/viewtodo.html', {'todo': todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('userhome')
        except ValueError:
            return render(request, 'app1/viewtodo.html', {'todo': todo, 'form':form, 'Error':'Bad info. Please Retry.'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('userhome')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('userhome')
