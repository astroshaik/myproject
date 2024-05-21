from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .serializers import RoomieSerializer
from .serializers import TaskSerializer
from .serializers import RuleSerializer
from .models import Roomie
from .models import Task
from .models import Rule
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomieRegistrationSerializer

class RoomieView(generics.CreateAPIView):
    queryset = Roomie.objects.all()
    serializer_class = RoomieSerializer
class TaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
class RuleView(generics.CreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    
class RoomieRegistrationView(generics.CreateAPIView):
    serializer_class = RoomieRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            roomie = serializer.save()
            # If valid, save and return relevant information
            return Response({
                "roomie_id": roomie.roomie_id,
                "email": roomie.email
            }, status=status.HTTP_201_CREATED)
        # If data is invalid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)