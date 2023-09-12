from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Account, Category, Transaction, Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import models
from datetime import datetime


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

@login_required
def dashboardView(request):
    user = request.user
    account = Account.objects.get(user=user)
    categories = Category.objects.all()
    
    if request.method == "POST":
        purpose = request.POST.get("purpose")
        amount = request.POST.get("Amount")
        category_name = request.POST.get("category")
        date = request.POST.get('date')
        category = Category.objects.get(name=category_name)
        
        expense = Expense(user=account, purpose=purpose, amount=amount, category=category, date=date) 
        expense.save()
        return redirect("dashboard")       
    # Calculate the total balance (sum of deposits - sum of withdrawals - sum of transfers)
    total_balance = Transaction.objects.filter(user=account).aggregate(
        total_deposits=Sum('amount', filter=models.Q(transaction_type='deposit')),
        total_withdrawals=Sum('amount', filter=models.Q(transaction_type='withdraw')),
        total_transfers=Sum('amount', filter=models.Q(transaction_type='transfer'))
    )
    total_balance = (total_balance['total_deposits'] or 0) - (total_balance['total_withdrawals'] or 0) - (total_balance['total_transfers'] or 0)

    # Calculate the total expenses
    # total_expenses = Expense.objects.filter(user=account).aggregate(total_expenses=Sum('amount'))
    # total_expenses = total_expenses['total_expenses'] or 0
    current_date = datetime.now()
    current_month = current_date.month
    
    total_expenses = Expense.objects.filter(
        user=account,
        date__month=current_month
    ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
    total_balance = total_balance - total_expenses
    
    
    
    total_income = Transaction.objects.filter(
        transaction_type='deposit',
        date__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    
    
    context = {
        "categories": categories,
        "total_balance": total_balance,
        "total_expenses": total_expenses,
        "current_date": current_date,
        "total_income": total_income
    }
    return render(request, 'dashboard.html', context=context)

@login_required
def cardDetailsView(request):
    categories = Category.objects.all()
    transactions = Transaction.objects.all()
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        transaction_type = request.POST.get('type')
        amount = request.POST.get('Amount')
        purpose = request.POST.get('purpose')
        date = request.POST.get('date')
        
        transaction = Transaction(user=account, transaction_type=transaction_type, amount=amount, purpose=purpose, date=date)
        transaction.save()
        return redirect("dashboard")
    total_balance = Transaction.objects.filter(user=account).aggregate(
        total_deposits=Sum('amount', filter=models.Q(transaction_type='deposit')),
        total_withdrawals=Sum('amount', filter=models.Q(transaction_type='withdraw')),
        total_transfers=Sum('amount', filter=models.Q(transaction_type='transfer'))
    )
    total_balance = (total_balance['total_deposits'] or 0) - (total_balance['total_withdrawals'] or 0) - (total_balance['total_transfers'] or 0)

    # Calculate the total expenses
    total_expenses = Expense.objects.filter(user=account).aggregate(total_expenses=Sum('amount'))
    total_expenses = total_expenses['total_expenses'] or 0
    total_balance = total_balance - total_expenses
    
    current_date = datetime.now()
    
    context = {"categories": categories, "transactions": transactions, "total_balance": total_balance,
        "total_expenses": total_expenses, "current_date": current_date}
    return render(request, 'card-details.html', context)

def categoryView(request):
    return render(request, 'category.html')

