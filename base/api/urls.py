from django.urls import path
from . import views

# Define your URL patterns here.
urlpatterns = [
    path('' , views.get_Routes),
    path('rooms/' , views.get_rooms),
    path('rooms/<str:pk>/' , views.get_room),
]