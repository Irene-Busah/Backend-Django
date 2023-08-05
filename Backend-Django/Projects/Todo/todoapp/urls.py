from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('todos/', views.todo_list, name='todos'),
    path('create_todo/', views.create_todo, name='add_item'),
    path('edit_task/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
    path('complete/<int:pk>/', views.mark_task_complete, name='mark_task_complete'),
    path('incomplete/<int:pk>/', views.mark_task_incomplete, name='mark_task_incomplete'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.sign_up, name='sign_up'),
    path('login_view/', views.login_view, name='login_view'),
]