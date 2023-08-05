from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('event/<str:pk>/', views.event_page, name='event'),
    path('event-confirmation/<str:pk>', views.registration_confirmation, name='event-confirm'),
    path('profile/<str:pk>/', views.user_page, name='profile'),
    path('account/', views.account_page, name='user-account'),
    path('project-submission/<str:pk>', views.project_submission, name='project_submission')
]