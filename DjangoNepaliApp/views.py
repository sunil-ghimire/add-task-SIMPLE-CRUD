from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from django.core.files.storage import FileSystemStorage
from DjangoNepaliApp.models import Notes
from django.contrib.auth.decorators import login_required


# Create your views here.
def demoPage(request):
    return HttpResponse('demoPage1.html')


def demoPage2(request):
    return render(request, 'demoPage1.html')


def LoginUser(request):
    if request.user != None:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'login.html')


def signupUser(request):
    return render(request, 'signup.html')


def signup_process(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
        user = User.objects.create(username=username, password=password, email=email, first_name=first_name,
                                   last_name=last_name)
        user.set_password(password)  # this will encrypt the password while saving in database
        user.save()
        messages.success(request, 'User signup successful')
    else:
        messages.error(request, 'Username or email already exists')

    return HttpResponseRedirect(reverse('signup'))


def login_process(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user != None:
        login(request, user)
        # messages.success(request, 'Login Successful')
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.error(request, 'Invalid login details')
        return HttpResponseRedirect(reverse('login'))


@login_required(login_url='/')
def home(request):
    all_tasks = Notes.objects.filter(user_id=request.user.id)
    return render(request, 'home.html', {'all_tasks': all_tasks})


def logoutUser(request):
    logout(request)
    request.user = None
    messages.error(request, 'Logout Successfully')
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='/')
def add_tasks(request):
    title = request.POST.get('title')
    task = request.POST.get('task')
    thumbnail = request.FILES['thumbnail']

    fs = FileSystemStorage()
    thumbnail_path = fs.save(thumbnail.name, thumbnail)

    current_user = User.objects.get(id=request.user.id)
    note = Notes(title=title, notes_data=task, user_id=current_user, thumbnail=thumbnail_path)
    note.save()
    messages.success(request, 'Task Added Successfully')
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='/')
def delete_task(request, id):
    task = Notes.objects.get(id=id)
    task.delete()
    messages.error(request, 'Task Deleted')
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='/')
def update_task(request, id):
    task = Notes.objects.get(id=id)
    return render(request, 'edit_task.html', {'task': task})


@login_required(login_url='/')
def edit_tasks_save(request, id):
    title = request.POST.get('title')
    task_data = request.POST.get('task')

    # update data in models
    task = Notes.objects.get(id=id)
    task.title = title
    task.notes_data = task_data
    task.save()
    messages.success(request, 'Task Updated')
    # return HttpResponseRedirect(reverse('update_task', kwargs={'id': id}))
    return HttpResponseRedirect(reverse('home'))
