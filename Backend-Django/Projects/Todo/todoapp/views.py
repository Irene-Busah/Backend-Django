from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

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
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos')
    context = {'form': form}
    return render(request, 'add_item.html', context=context)

def edit_task(request, pk):
    task_item = Task.objects.get(pk=pk)
    form = TaskForm(instance=task_item)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task_item)
        if form.is_valid():
            form.save()
            return redirect('todos')
    else:
        form = TaskForm(instance=task_item)
    return render(request, 'edit_task.html', {'form': form, 'task': task_item})

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