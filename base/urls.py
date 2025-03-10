from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    # User related urls
    path('user/profile/<str:pk>/', views.UserProfile , name='profile'),
    path('user/login/', views.LoginView, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    path('user/register/', views.registerView, name='register'),
    path('user/edit-user/<str:pk>/', views.edit_userView, name='edit'),
    
    # Home Page URL
    path('', views.home, name='home'),
    path('room/create-room/', views.CreateRoom, name='create-room'),
    path('room/update-room/<str:pk>/', views.UpdateRoom, name='UpdateRoom'),
    path('room/delete-room/<str:pk>/', views.DeleteRoom, name='DeleteRoom'),
    path('room/<str:pk>/', views.Room, name='room'),

    # Urls for the messages 
    # path('message/', views.addMessage , name='addMessage'),
    path('messages/<str:pk>/', views.UpdateMessage, name='update_message'),
    path('messages/delete-message/<str:pk>/', views.DeleteMessage, name='delete_message'),

    # topics urls
    path('topics/' , views.topics, name='topics'),
    path('activity/' , views.activity, name='activity'),
]
