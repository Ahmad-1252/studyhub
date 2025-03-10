from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Rooms, Topic, Message, User
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# user models views

def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.rooms_set.all()
    messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user' : user, 'room_messages' : messages, 'rooms' : rooms, 'topics' : topics}
    return render(request, 'base/user_profile.html', context)

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "username or password does not exist")
        except :
            messages.error(request, "Invalid username or password")

    context = {'page': 'login'}
    return render(request, 'base/login_register.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def registerView(request):
    if request.method == 'POST':
        data = request.POST
        if data.get('password') == data.get('confirm_password'):
            if User.objects.filter(username=data.get('username')):
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                
                profile_picture = request.FILES.get('profile_picture')  # ✅ Get the uploaded file

                user = User.objects.create(
                    first_name=data.get('firstname'),
                    last_name=data.get('lastname'),
                    username=data.get('username'),
                    email=data.get('email'),
                    bio = data.get('bio'),
                    password=data.get('password'),
                    profile_picture=profile_picture
                )
                messages.success(request, 'Account created successfully')
                login( request, user)
                return redirect('/')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    context = {'page' : 'register'}
    return render(request, 'base/login_register.html', context)

def edit_userView(request, pk):
    user = User.objects.get(id=pk)

    try:
        if request.method == 'POST':
            if request.FILES.get('profile_picture'):
                user.profile_picture =  request.FILES.get('profile_picture')
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.bio = request.POST.get('bio')
            user.email = request.POST.get('email')

            user.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('/')
    except Exception as e:
        messages.error(request, str(e))

    context = {'user': user , 'page': 'register', 'updation'  : 1}
    return render(request, 'base/login_register.html', context)

# common Functions for the vuews
def save_room(request, pk= None):
    if request.method == 'POST':
        data = request.POST
        topic, create = Topic.objects.get_or_create(title = data.get('topic'))
        try:
            Room.objects.create({
                'name' : data.get('name'),
                'description' : data.get('description'),
                'topic' : topic,
                'host' : request.user,   
            })
        except:
            messages.error(request, 'Error occurred while creating room')
        if pk is not None:
            room_instance = Rooms.objects.get(id=pk)
            roomForm = RoomForm(data, instance=room_instance)
        else:
            roomForm = RoomForm(data)
        if roomForm.is_valid():
            room = roomForm.save(commit=False)
            room.host = request.user
            room.save()
            return room.id
    else:
        return False    

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Rooms.objects.filter(Q(topic__title__icontains=q)
                                 | Q(name__icontains=q)
                                 | Q(description__icontains=q))
    paginator = Paginator(rooms, 5)
    page_number = request.GET.get('page')
    page_rooms = paginator.get_page(page_number)
    all_topics = Topic.objects.all()
    topics_paginator = Paginator(all_topics, 4)
    topics = topics_paginator.get_page(page_number)
    messages = Message.objects.filter(room__in=page_rooms.object_list)

    context = {'rooms' : page_rooms, 'topics' : topics , 'room_messages' : messages , 'topic_count': all_topics.count()}
    return render(request, 'base/home.html', context)

def Room(request, pk):
    room = Rooms.objects.get(pk=pk)
    if request.method == 'POST':
        user = request.user
        try:
            message = Message.objects.create(
                user = user,
                room = room,
                body = request.POST.get('body')
                )
            # append the onwer of the message as a new participant 
            if room.host != user:
                room.participants.add(request.user)
            messages.success(request, 'Message sent successfully')
            return redirect('room' , pk=room.id)
        except:
            messages.error(request, 'Error occurred while creating message')
        
    # we can get the children of this room by specifying the childs name
    room_messages = room.message_set.all()
    context = {'room' : room , 'message': room_messages}
    return render(request , 'base/room.html', context)

@login_required(login_url='login')
def CreateRoom(request):
    if request.method == 'POST':
        data = request.POST
        topic, created = Topic.objects.get_or_create(title = data.get('topic'))
        try:
            Rooms.objects.create(
                name = data.get('room_name'),
                description = data.get('description'),
                topic = topic,
                host = request.user,   
            )
            return redirect('home')
        except Exception as e:

            messages.error(request, f'Error occurred while creating room\n{e}')
    context = {'topics' : Topic.objects.all()}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Rooms.objects.get(pk=pk)
    roomForm = RoomForm(instance=room)
    if request.method == 'POST':
        topic_input = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(title= topic_input)
        room.topic = topic
        room.name = request.POST.get('room_name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('/room/' + pk)
    context = {'roomForm': roomForm , 'topics' : Topic.objects.all(), 'room' : room}
    return render(request, 'base/room_form.html', context)
    
@login_required(login_url='login') 
def DeleteRoom(request, pk):
    if pk:
        room = Rooms.objects.get(pk=pk)
        if request.method == 'POST':
            room.delete()
            return HttpResponseRedirect('/')
    return render(request, 'base/delete_room.html', {'room': room})


# Messages views

# def addMessage(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.user = request.user
#             message.room_id = request.POST.get('room_id')
#             message.save()
#             return redirect('room' + str(message.room_id))
#     return HttpResponseRedirect('/')

def UpdateMessage(request , pk):
    pass

@login_required(login_url='login')
def DeleteMessage(request , pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        if request.user == message.user:
            message.delete()
            return redirect('room' , message.room_id)
        else:
            return HttpResponse('You are not allowed to delete this message')
    context = {'message': message}
    return render(request, 'base/delete_room.html' , context)


# topics view
def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    room_count = Rooms.objects.filter(Q(topic__title__icontains=q)
                                 | Q(name__icontains=q)
                                 | Q(description__icontains=q)).count()
    topics = Topic.objects.filter(title__icontains=q)
    context = {'topics': topics, 'room_count': room_count}
    return render(request, 'base/topics.html', context)

    
def activity(request):
    rooms = Rooms.objects.all()
    messages = Message.objects.all()
    context = {'rooms': rooms, 'room_messages': messages}
    return render(request, 'base/activity.html', context)