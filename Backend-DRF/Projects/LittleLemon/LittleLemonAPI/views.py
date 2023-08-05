from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth.admin import User, Group
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer, MenuItemSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from .models import *
from datetime import date

# ======================= User group management endpoints =====================

@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manager(request, user_id=None):
    manager_group = Group.objects.get(name='Manager')
    
    if request.method == 'GET':
        if user_id:
            user = User.objects.get(id=user_id)
            if user is not None:
                manager = manager_group.user_set.get(id=user.id)
                serialized_item = UserSerializer(manager)
                return JsonResponse({'Manager': serialized_item.data})
            
        managers = manager_group.user_set.all()
        serialized_item = UserSerializer(managers, many=True)
        return JsonResponse({'managers': serialized_item.data}, status=status.HTTP_200_OK, safe=False)
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            manager_group.user_set.add(user)
            return JsonResponse({'success': True}, status=201)
    
    elif request.method == 'DELETE' and user_id:
        try:
            user = User.objects.get(id=user_id)
            manager_group.user_set.remove(user)
            return JsonResponse({'success': True}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['POST', 'GET', 'DELETE'])
@login_required
def delivery_crew(request, user_id=None):
    delivery_crew_group = Group.objects.get(name='Delivery crew')
    
    if request.method == 'GET':
        delivery_crew = delivery_crew_group.user_set.all()
        serialized_crew = UserSerializer(delivery_crew, many=True)
        return JsonResponse({'Delivery crew': serialized_crew.data}, status=200)
    elif request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists():
            username = request.POST.get('username')
            user = get_object_or_404(User, username=username)
            delivery_crew_group.user_set.add(user)
            return JsonResponse({'success': True}, status=201)
        else:
            return JsonResponse({'error': 'You are not authorized to perform this action'}, status=403)
        
    elif request.method == 'DELETE' and user_id:
        try:
            user = User.objects.get(id=user_id)
            delivery_crew_group.user_set.remove(user)
            return JsonResponse({'success': True}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User is not found'}, status=404)
        
        
# ========================== Menu-items endpoints ==========================
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@login_required
def menuItems(request, menuItem=None):
    if request.method == 'GET':
        if menuItem:
            try:
                item = MenuItem.objects.get(title=menuItem)
                serialized_item = MenuItemSerializer(item)
                return JsonResponse({'menuItem': serialized_item.data}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Item not found'}, status=404)
        menu_items = MenuItem.objects.all()
        serialized_items = MenuItemSerializer(menu_items, many=True)
        return JsonResponse({'Menu items': serialized_items.data}, status=200)
    if request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists():
            data = request.data
            serializer = MenuItemSerializer(data=data)
            
            if serializer.is_valid():
                menu_item = serializer.save()
                return JsonResponse({'success': True, 'menu item': menu_item.title}, status=201)
        else:
            return JsonResponse({'error': 'You are not authorized to perform this action'}, status=403)

    if request.method == 'PUT' and menuItem:
        if request.user.groups.filter(name='Manager').exists():
            item = MenuItem.objects.get(title=menuItem)
            data = request.data
            serializer = MenuItemSerializer(instance=item, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'success': True, 'menu item': item.title}, status=200)
        else:
            return JsonResponse({'error': 'You are not authorized to perform this action'}, status=403)
        
        
    if request.method == 'PATCH' and menuItem:
        if request.user.groups.filter(name='Manager').exists():
            item = MenuItem.objects.get(title=menuItem)
            data = request.data
            serializer = MenuItemSerializer(instance=item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'success': True, 'menu item': item.title}, status=200)
        else:
            return JsonResponse({'error': 'You are not authorized to perform this action'}, status=403)
    
    
    if request.method == 'DELETE' and menuItem:
        if request.user.groups.filter(name='Manager').exists():
            try:
                item = MenuItem.objects.get(title=menuItem)
                item.delete()
                return JsonResponse({'success': True, 'message': f'{item.title} deleted'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Item is not found'})
        else:
            return JsonResponse({'error': 'You are not authorized to perform this action'}, status=403)



# ========================= Cart management endpoints ==========================
@api_view(['GET', 'POST', 'DELETE'])
@login_required
def cartItems(request):
    user = request.user
    if request.method == 'GET':
        if user.groups.filter(name__in=['Delivery crew', 'Manager']).exists():
            return JsonResponse({'error': 'Access denied'}, status=403)
        else:
            cart_items = Cart.objects.filter(user=user)
            serializer = CartItemSerializer(cart_items, many=True)
            return JsonResponse({'Cart Items': serializer.data}, status=200)
    
    if request.method == 'POST':
        if user.groups.filter(name__in=['Delivery crew', 'Manager']).exists():
            return JsonResponse({'error': 'Access denied'}, status=403)
        else:
            menuitem_id = request.POST.get('menuitem')
            quantity = int(request.POST.get('quantity'))
            menuitem = MenuItem.objects.get(id=menuitem_id)
            unit_price = menuitem.price
            price = unit_price * quantity
            
            cart_item = Cart.objects.create(user=user, menuitem=menuitem, quantity=quantity, unit_price=unit_price, price=price)
            
            return JsonResponse({'success': True, 'message': 'Item added to cart'}, status=201)
    
    
    if request.method == 'DELETE':
        if user.groups.filter(name__in=['Delivery crew', 'Manager']).exists():
            return JsonResponse({'error': 'Access denied'}, status=403)
        else:
            items = Cart.objects.all()
            if items:
                items.delete()
                return JsonResponse({'Success': True, 'message': 'Cart is Empty!'}, status=200)
            else:
                return JsonResponse({'message': 'Empty Cart!!'}, status=200)
            


# ======================= Order management endpoints ========================
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@login_required
def get_orders(request, orderId=None):
    user = request.user
    
    if request.method == 'GET':
        if not user.groups.filter(name__in=['Delivery crew', 'Manager']).exists():
            # Customer - GET /api/orders/{orderId}
            if orderId:
                try:
                    order = Order.objects.get(id=orderId, user=user)
                    order_items = OrderItem.objects.filter(order=order)
                    serializer = OrderItemSerializer(order_items, many=True)
                    return JsonResponse({'order': OrderSerializer(order).data, 'order_items': serializer.data}, status=200)
                except Order.DoesNotExist:
                    return JsonResponse({'error': 'Order not found'}, status=404)
                except PermissionDenied:
                    return JsonResponse({'error': 'Unauthorized user'}, status=403)
            # Customer - GET /api/orders
            else:
                orders = Order.objects.filter(user=user)
                serializer = OrderSerializer(orders, many=True)
                return JsonResponse({'orders': serializer.data}, status=200)
        
        elif user.groups.filter(name='Delivery crew').exists():
            # Delivery crew - GET /api/orders
            orders = Order.objects.filter(delivery_crew=user)
            serializer = OrderSerializer(orders, many=True)
            return JsonResponse({'orders': serializer.data}, status=200)
        
        elif user.groups.filter(name='Manager').exists():
            # Manager - GET /api/orders
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return JsonResponse({'orders': serializer.data}, status=200)
        
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    elif request.method == 'POST':
        if not user.groups.filter(name__in=['Delivery crew','Manager']).exists():
        # Get current cart items for the user
            cart_items = Cart.objects.filter(user=user)
            
            # Calculate the total by summing the prices of each item
            total = sum(item.price for item in cart_items)
            if cart_items.exists():
                # Create a new order
               
                order = Order.objects.create(user=user, delivery_crew=None, status=1, total=total, date=date.today())
                
                # Create order items based on the cart items
                order_items = []
                for cart_item in cart_items:
                    menuitem = request.POST.get('menuitem')
                    quantity = request.POST.get('quantity')
                    unit_price = request.POST.get('unit_price')
                    price = request.POST.get('price')
                    
                    order_item = OrderItem.objects.create(
                        order=order,
                        menuitem=cart_item.menuitem,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.unit_price,
                        price=cart_item.price
                    )
                    
                
                # Delete cart items for the user
                cart_items.delete()
                
                serializer = OrderItemSerializer(order_items, many=True)
                return JsonResponse({'order_items': serializer.data, 'success': True}, status=201)
            else:
                return JsonResponse({'error': 'Cart is empty'}, status=400)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
    elif request.method == 'PATCH' and orderId or request.method == 'PUT' and orderId:
        user = request.user
        order = Order.objects.get(id=orderId)
        data = request.data
        if user.groups.filter(name=('Manager')).exists():
            delivery_crew_id = request.data.get('delivery_crew')
            status = request.data.get('status')
            
            # Validate the data
            if delivery_crew_id is not None:
                # Check if the delivery crew exists
                delivery_crew = get_object_or_404(User, id=delivery_crew_id)
                order.delivery_crew = delivery_crew
            if status is not None:
                order.status = status
            # Save the updated order
            order.save()
            # ensure that the manager can update only the delivery crew & status fields
            serializer = OrderSerializer(instance=order, data=data, partial=True)
            if serializer.is_valid():
                serializer.update(order, serializer.validated_data)
                serializer.save()
                return JsonResponse({'order': serializer.data}, status=200)
    
            return JsonResponse({'order': serializer.data}, status=200)
        
        if user.groups.filter(name=('Delivery crew')).exists():
            status = request.data.get('status')
            if status is not None:
                order.status = status
            # Save the updated order
            order.save()
            serializer = OrderSerializer(instance=order, data=data, partial=True)
            if serializer.is_valid():
                serializer.update(order, serializer.validated_data)
                serializer.save()
                return JsonResponse({'order': serializer.data}, status=200)
            
    elif request.method == 'DELETE' and orderId:
        if request.user.groups.filter(name='Manager').exists():
            try:
                item = Order.objects.get(id=orderId)
                item.delete()
                return JsonResponse({'success': True, 'message': f'{item.user} deleted'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Order is not found'})
        else:
            return JsonResponse({'error': 'You are not authorized to perform this action'}, status=403)
            
