from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Rooms
from .serializers import RoomSerializer

@api_view(['GET'])
def get_Routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/room/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def get_rooms(request):
    rooms = Rooms.objects.all()
    serialized_data = RoomSerializer(rooms, many=True)
    return Response(serialized_data.data)


@api_view(['GET'])
def get_room(request , pk):
    try:
        room = Rooms.objects.get(id=pk)
    except Rooms.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
    serialized_data = RoomSerializer(room, many=False)
    return Response(serialized_data.data) 