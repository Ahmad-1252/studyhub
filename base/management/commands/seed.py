from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from base.models import Topic, Rooms, Message
from django.core.files import File
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with test data"

    def handle(self, *args, **kwargs):
        # 1️⃣ Create Users
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')
            self.stdout.write(self.style.SUCCESS('✔ Admin user created!'))
        else:
            admin_user = User.objects.get(username='admin')

        user1, created = User.objects.get_or_create(username="Ali", email="ali@gmail.com")
        user1.set_password("password123")
        user1.save()

        user2, created = User.objects.get_or_create(username="Omar", email="omar@gmail.com")
        user2.set_password("password123")
        user2.save()

        self.stdout.write(self.style.SUCCESS('✔ Users created!'))

        # 2️⃣ Create Topics
        topic1, _ = Topic.objects.get_or_create(title="Technical Writing")
        topic2, _ = Topic.objects.get_or_create(title="Java")
        topic3, _ = Topic.objects.get_or_create(title="C++ Development")

        self.stdout.write(self.style.SUCCESS('✔ Topics created!'))

        # 3️⃣ Create Rooms
        room1, _ = Rooms.objects.get_or_create(
            host=admin_user,
            topic=topic2,
            name="Master Java with me!",
            description="Discuss the latest in tech."
        )

        room2, _ = Rooms.objects.get_or_create(
            host=user1,
            topic=topic1,
            name="Dicuss the latest tools for technical writing",
            description="Exploring different tool for writing."
        )

        room3, _ = Rooms.objects.get_or_create(
            host=user2,
            topic=topic3,
            name="Game Development with C++",
            description="All about game developement."
        )

        room1.participants.add(user1, user2)
        room2.participants.add(admin_user)
        room3.participants.add(admin_user, user1)

        self.stdout.write(self.style.SUCCESS('✔ Rooms created!'))

        # 4️⃣ Create Messages
        Message.objects.create(user=admin_user, room=room1, body=f"Welcome to the '{room1.name}'")
        Message.objects.create(user=user1, room=room2, body="Let's discuss the writing techniques with each other.")
        Message.objects.create(user=user2, room=room3, body="Which game are you playing these days? Are you wanna develop a new game.")

        self.stdout.write(self.style.SUCCESS('✔ Messages created!'))
