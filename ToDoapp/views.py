from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.cache import never_cache, cache_control

from ToDoapp.forms import Taskform
from ToDoapp.models import Task

@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def regpage(request):
    return render(request,'register.html')


@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def regdata(request):
    user = request.POST['user']
    mail = request.POST['mail']
    password = request.POST['epass']
    cpassword = request.POST['cpass']
    if User.objects.filter(Q(username=user) | Q(email=mail)).exists():
        return render(request,'register.html',{'data':'Username or Email already exists'})
    else:
        if password==cpassword:
            u1 = User.objects.create_superuser(username=user,email=mail,password=password)
            u1.save()
            return redirect('log')
        else:
            return render(request,'register.html',{'data':'Passwords does not match'})


@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def log_fun(request):
    return render(request,'login.html',{'data':''})

@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def login_fun(request):
    user = request.POST['txtuser']
    mail = request.POST['txtuser']
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


@login_required
@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def home_fun(request):
    tasks = Task.objects.all()
    count = tasks.filter(complete=False).count()
    return render(request,'home.html',{'tasks':tasks,'count':count})


@login_required
@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def add_task(request):
    if request.method == 'POST':
        form = Taskform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasklist')
    else:
        form = Taskform()
    return render(request, 'addtask.html', {'form': form})


@login_required
@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
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


@login_required
@cache_control(no_cache=True,revalidate=True,nostore=True)
@never_cache
def delete_task(request,pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('tasklist')


def logout_fun(request):
    logout(request)
    return redirect('log')