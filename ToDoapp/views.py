from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.cache import never_cache, cache_control

from ToDoapp.forms import Taskform
from ToDoapp.models import Task


def regpage(request):
    return render(request,'register.html')


@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def regdata(request):
    user = request.POST['user']
    password = request.POST['epass']
    cpassword = request.POST['cpass']
    if User.objects.filter(Q(username=user)).exists():
        return render(request,'register.html',{'data':'Username or Email already exists'})
    else:
        if password==cpassword:
            u1 = User.objects.create_superuser(username=user,password=password)
            u1.save()
            return redirect('log')
        else:
            return render(request,'register.html',{'data':'Passwords does not match'})


def log_fun(request):
    return render(request,'login.html',{'data':''})


def login_fun(request):
    user = request.POST['txtuser']
    pswd = request.POST['txtpass']
    user1 = authenticate(username=user,password=pswd)
    if user1 is not None:
        if user1.is_superuser:
            login(request,user1)
            return redirect('tasklist')
        else:
            return render(request,'login.html',{'data':'User is not superuser'})
    else:
        return render(request, 'login.html', {'data': 'your username and password are not matching'})


def home_fun(request):
    tasks = Task.objects.all()
    return render(request,'home.html',{'tasks':tasks})



def add_task(request):
    if request.method == 'POST':
        form = Taskform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasklist')
    else:
        form = Taskform()
    return render(request, 'addtask.html', {'form': form})


def edit_task(request,pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = Taskform(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasklist')
    else:
        form = Taskform(instance=task)
    return render(request, 'edittask.html', {'form': form, 'task': task})


def delete_task(request,pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('tasklist')