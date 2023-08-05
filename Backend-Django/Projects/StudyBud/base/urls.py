from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.delete_message, name="delete_message"),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topics_page, name='topics'), 
    path('activity/', views.activities_page, name='activity')
]
