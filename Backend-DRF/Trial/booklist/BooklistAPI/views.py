from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Book
from .serializers import BookSerializer


# Create your views here.
# @api_view(['GET', 'POST'])
# def books(request):
#     if request.method == 'GET':
#         books = Book.objects.all().values()
#         return JsonResponse({'Books': list(books)})
#     elif request.method == 'POST':
#         title = request.POST.get('title')
#         author = request.POST.get('author')
#         price = request.POST.get('price')
        
#         book = Book(title=title, author=author, price=price)
#         try:
#             book.save()
#         except IntegrityError:
#             return JsonResponse({'error':'true','message':'required field missing'})
#         return JsonResponse(model_to_dict(books))
        

class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class SingleBookView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
