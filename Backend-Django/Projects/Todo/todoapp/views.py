from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
# from celery import shared_task
# from datetime import datetime
# from django.utils import timezone
# from django.core.mail import send_mail

# @shared_task
# def send_task_reminders():
#     now = timezone.now()
#     overdue_tasks = Task.objects.filter(completion_time__lte=now, complete=False)

#     for task in overdue_tasks:
#         user_email = task.user.email if task.user else None
#         if user_email:
#             send_mail(
#                 'Task Reminder',
#                 f'Reminder: Your task "{task.title}" is overdue!',
#                 'your_email@example.com',  # Sender's email address
#                 [user_email],  # Recipient's email address
#                 fail_silently=False,
#             )
#         task.complete = True
#         task.save()

# Create your views here.
def index(request):
    return render(request, 'home.html')

@login_required
def todo_list(request):
    # listing all the items
    todo_list = Task.objects.filter(user=request.user)
    user = request.user.username
    context = {'todo': todo_list, 'user': user}
    return render(request, 'list.html', context=context)

def create_todo(request):
    user = request.user
    title = request.POST.get("title")
    description = request.POST.get("description")
    # print(user, title, description)
    if user and title:
        todo = Task(user=user, title=title, description=description)
        todo.save()
        return redirect('todos')
    return render(request, 'add_item.html')

def edit_task(request, pk):
    task_item = Task.objects.get(pk=pk)
    # form = TaskForm(instance=task_item)
    if request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")
    
        if title:
            task_item.title = title
            task_item.description = description
            task_item.save()
            return redirect('todos')
    return render(request, 'edit_task.html', {'task': task_item})

def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('todos')

def mark_task_complete(request, pk):
    task = Task.objects.get(pk=pk)
    task.complete = True
    task.save()
    return redirect('todos')
def mark_task_incomplete(request, pk):
    task = Task.objects.get(pk=pk)
    task.complete = False
    task.save()
    return redirect('todos')

def logout_view(request):
    logout(request)
    return redirect('home')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.get(username=username)
                return render(request, 'register.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('todos')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'register.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todos')
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')