from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .serializers import RoomieSerializer
from .models import Roomie

class RoomieView(generics.ListAPIView):
    queryset = Roomie.objects.all()
    serializer_class = RoomieSerializer