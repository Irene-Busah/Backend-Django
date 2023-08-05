from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MenuItem, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MenuItemSerializer, CategorySerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from django.contrib.auth.admin import User, Group

# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# @api_view(['GET', 'POST'])
# def menu_items(request):
#     if request.method == 'GET':
#         menus = MenuItem.objects.select_related('category').all()
#         category_name = request.query_params.get('category')
#         to_price = request.query_params.get('to_price')
#         search = request.query_params.get('search')
#         ordering = request.query_params.get('ordering')
#         perpage = request.query_params.get('perpage', default=2)
#         page = request.query_params.get('page', default=1)
#         if category_name:
#             menus = menus.filter(category__title=category_name)
#         if to_price:
#             menus = menus.filter(price__lte=to_price)
#         if search:
#             menus = menus.filter(title__contains=search)
#         if ordering:
#             menus = menus.order_by(ordering)
#         paginator = Paginator(menus, per_page=perpage)
#         try:
#             menus = paginator.page(number=page)
#         except EmptyPage:
#             menus = []
#         serialized_item = MenuItemSerializer(menus, many=True)
#         return Response(serialized_item.data)
#     if request.method == 'POST':
#         serialized_item = MenuItemSerializer(data=request.data)
#         serialized_item.is_valid(raise_exception=True)
#         serialized_item.save()
#         return Response(serialized_item.validated_data, status=HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message': 'Some secret key'})

@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def manager(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == "POST":
            managers.user_set.add(user)
        elif request.method == "DELETE":
            managers.user_set.remove(user)
        
        return Response({'message': 'Okay'})
    return Response({"message": "Error"}, status.HTTP_400_BAD_REQUEST)
