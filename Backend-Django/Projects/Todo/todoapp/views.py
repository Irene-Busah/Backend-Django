from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from .tasks import send_task_reminders, send_task_notification


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
    date = request.POST.get("date")
    
    if user and title:
        todo = Task(user=user, title=title, completion_time=date, description=description)
        todo.save()
        subject = f'Task Created: {todo.title}'
        message = f'You have created a new task:\n\nTitle: {todo.title}\n\nCompletion Date: {todo.completion_time}\n\n\nAll the Best to accomplish your goals!'
        send_task_notification.delay(todo.id, subject, message)
        return redirect('todos')
    return render(request, 'add_item.html')

def edit_task(request, pk):
    task_item = Task.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST.get("title")
        date = request.POST.get("date")
        description = request.POST.get("description")
        
        if title:
            task_item.title = title
            task_item.completion_time = date
            task_item.description = description
            task_item.save()
            subject = f'Task Edited: {task_item.title}'
            message = f'You have edited the task:\n\nTitle: {task_item.title}\n\nCompletion Date: {task_item.completion_time}\n\n\nAll the Best to accomplish your goals!'
            send_task_notification.delay(task_item.id, subject, message)
            return redirect('todos')
    return render(request, 'edit_task.html', {'task': task_item})

def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    subject = f'Task Deleted: {task.title}'
    message = f'You have deleted the task:\n\nTitle: {task.title}\n\n\nGo ahead and add more tasks!'
    send_task_notification.delay(pk, subject, message)
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
            send_task_reminders.delay()
            return redirect('todos')
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')