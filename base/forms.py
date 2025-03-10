from django.forms import ModelForm
from .models import Rooms, Message
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'
        exclude = ['host' , 'participants']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')