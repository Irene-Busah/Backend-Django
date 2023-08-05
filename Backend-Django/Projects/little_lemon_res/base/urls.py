from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.display_menu_items, name='menu_item'),
    path('book_list/', views.display_bookings, name='book_list'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.sign_up, name='sign_up'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('delete_menu/<int:pk>/', views.delete_menu, name='delete_menu'),
    path('update_menu/<int:pk>/', views.update_menu, name='update_menu')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
