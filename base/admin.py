from django.contrib import admin
from .models import Rooms, Topic, Message, User
# Register your models here.

admin.site.register([Rooms, Topic, Message, User])