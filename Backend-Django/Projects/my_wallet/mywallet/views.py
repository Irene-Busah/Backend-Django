from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Account, Category, Transaction
from django.contrib.auth.decorators import login_required
# Create your views here.

def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(username, password, user)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, "login.html")

def registerView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("cpassword")
        profile_pic = request.FILES.get("image")
        
        if password == confirm_password:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
            account = Account.objects.create(user=user, profile_pic=profile_pic)
            account.save()
        
        return redirect("login")
    return render(request, 'register.html')

def dashboardView(request):
    categories = Category.objects.all()
    
    context = {"categories": categories}
    return render(request, 'dashboard.html', context=context)

@login_required
def cardDetailsView(request):
    categories = Category.objects.all()
    transactions = Transaction.objects.all()
    if request.method == 'POST':
        transaction_type = request.POST.get('type')
        amount = request.POST.get('Amount')
        purpose = request.POST.get('purpose')
        date = request.POST.get('date')
        account = Account.objects.get(user=request.user)
        transaction = Transaction(user=account, transaction_type=transaction_type, amount=amount, purpose=purpose, date=date)
        transaction.save()
        return redirect("dashboard")
    context = {"categories": categories, "transactions": transactions}
    return render(request, 'card-details.html', context)

def categoryView(request):
    return render(request, 'category.html')

