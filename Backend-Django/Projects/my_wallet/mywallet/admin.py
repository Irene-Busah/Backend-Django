from django.contrib import admin
from .models import Account, Transaction, Expense, Category

# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Expense)
admin.site.register(Category)
