from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
   path('menu-items', views.MenuItemView.as_view()),
   path('menu-item/<str:pk>', views.SingleMenuItemView.as_view()),
   path('category', views.CategoriesView.as_view()),
   path('secret', views.secret, name='menus'),
   path('api-token-auth/', obtain_auth_token),
   path('me/', views.me),
   path('groups/manager/users/', views.manager)
   # path('menu-items/', views.menu_items, name='menus')
]