from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        read_only_fields = ['user', 'delivery_crew', 'status', 'total', 'date']
        
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        # user = self.context['request'].user
        if request and request.user.groups.filter(name='Delivery crew').exists():
            fields['status'].read_only = False
        if request and request.user.groups.filter(name='Manager').exists():
            fields['delivery_crew', 'status'].read_only = False
        return fields

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']
