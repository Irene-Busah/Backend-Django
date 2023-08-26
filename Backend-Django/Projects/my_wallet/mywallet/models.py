from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile/', null=True, blank=True, default='../static/img/avatar.svg')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=15, default="#ff5c00")

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('deposit', 'Cash Deposit'),
        ('withdraw', 'Cash Withdraw'),
        ('transfer', 'Cash Transfer'),
    ]
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    purpose = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.user.first_name} - {self.amount}"

class Expense(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.purpose} - {self.amount}"
    

# https://www.youtube.com/watch?v=IC9mrBSe9B8
