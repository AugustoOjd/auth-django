from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# usa base de datos pre cargada sqlite3
from django.contrib.auth.models import User
# sent cookie session navegador
from django.contrib.auth import login, logout, authenticate
# error en base de datos
from django.db import IntegrityError
# modelo de formulario basado en objecto/class
from .forms import TaskForm

from .models import Task

# Create your views here.

from django.utils import timezone

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': ''
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                # return HttpResponse('user %s creado correctamente' % request.POST['username'])
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'user already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })


def tasks(request ):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # print(request.POST)
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            # print(new_task)
            return redirect('tasks')
        except:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Error invalid data'
            })

def task_detail(request, id):
    if request.method == 'GET':
        # task = list(Task.objects.filter(id=id))
        task = get_object_or_404(Task, pk=id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': 'error en actualizar'
            })
        

def complete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return('tasks')

def signout(request):
    logout(request)
    return redirect('home')


def sigin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        try:
            if user is None:
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'Invalid user'
                })
            else:
                # metodo login para guardar session en cookie
                login(request, user)
                return redirect('tasks')
        except:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Invalid credentials'
            })