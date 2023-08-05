from django.urls import path
from . import views

urlpatterns = [
    # path('api-token-auth/', obtain_auth_token),
    # Manager
    path('groups/manager/users/', views.manager, name='manager-users'),
    path('groups/manager/users/<int:user_id>/', views.manager, name='manager-users-detail'),
    
    # Delivery crew
    path('groups/delivery-crew/users', views.delivery_crew, name='delivery-crew'),
    path('groups/delivery-crew/users/<int:user_id>/', views.delivery_crew, name='delivery-crew-detail'),
    
    # Menu Items
    path('menu-items/', views.menuItems, name='menu'),
    path('menu-items/<str:menuItem>/', views.menuItems, name='menu'),
    # path('menu-items/', views.create_menu, name='create-menu'),
    
    # Cart Items
    path('cart/menu-items', views.cartItems, name='cart-items'),
    
    # Order Items
    path('orders', views.get_orders, name='order-list'),
    path('orders/<int:orderId>/', views.get_orders, name='order-item'),
]
