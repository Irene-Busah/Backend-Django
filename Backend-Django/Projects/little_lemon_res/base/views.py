from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Booking, Menu
from base.forms import BookingForm, MenuForm

# Create your views here.


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


@login_required(login_url='login_view')
def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'book.html', context=context)


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {'menu': menu_data}

    return render(request, 'menu.html', context=main_data)


def display_menu_items(request, pk=None):
    """view function for """
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    return render(request, 'menu_item.html', context={"menu_item": menu_item})


def delete_menu(request, pk):
    menu = Menu.objects.get(pk=pk)

    menu.delete()
    return redirect('menu')


def add_menu(request):
    form = MenuForm()
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')
    context = {'form': form}
    return render(request, 'addmenu.html', context=context)


def update_menu(request, pk):
    menu_item = Menu.objects.get(pk=pk)
    form = MenuForm(instance=menu_item)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuForm(instance=menu_item)
    return render(request, 'update_menu.html', {'form': form})


@login_required()
def display_bookings(request):
    """view function to display the list of people who have booked a reservation"""
    book_data = Booking.objects.all()
    book_items = {'book_list': book_data}

    return render(request, 'bookList.html', context=book_items)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.

            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


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
                return redirect('home')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'register.html')
