from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .serializers import RoomieSerializer
from .serializers import TaskSerializer
from .serializers import RuleSerializer
from .models import Roomie
from .models import Task
from .models import Rule

class RoomieView(generics.CreateAPIView):
    queryset = Roomie.objects.all()
    serializer_class = RoomieSerializer
class TaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
class RuleView(generics.CreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer