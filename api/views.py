# Import necessary Django and rest_framework classes
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Import serializers and models from the current application
from .serializers import RoomieSerializer, TaskSerializer, RuleSerializer, RoomieRegistrationSerializer
from .models import Roomie, Task, Rule

# CreateAPIView for creating a new Roomie instance
class RoomieView(generics.CreateAPIView):
    queryset = Roomie.objects.all()  # Defines the queryset that represents all Roomie objects
    serializer_class = RoomieSerializer  # Specifies the serializer to use for creating Roomie objects

# CreateAPIView for creating a new Task instance
class TaskView(generics.CreateAPIView):
    queryset = Task.objects.all()  # Defines the queryset that represents all Task objects
    serializer_class = TaskSerializer  # Specifies the serializer to use for creating Task objects

# CreateAPIView for creating a new Rule instance
class RuleView(generics.CreateAPIView):
    queryset = Rule.objects.all()  # Defines the queryset that represents all Rule objects
    serializer_class = RuleSerializer  # Specifies the serializer to use for creating Rule objects

# Custom CreateAPIView for handling registration of a new Roomie
class RoomieRegistrationView(generics.CreateAPIView):
    serializer_class = RoomieRegistrationSerializer  # Specifies the serializer for Roomie registration

    # Handles POST requests, overwriting the default post method
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Initializes the serializer with request data
        if serializer.is_valid():  # Checks if the provided data is valid per serializer's rules
            roomie = serializer.save()  # Saves the validated data into the database
            # Returns a success response with the roomie_id and email of the newly created Roomie
            return Response({
                "roomie_id": roomie.roomie_id,
                "email": roomie.email
            }, status=status.HTTP_201_CREATED)
        # If data is invalid, return the validation errors with a 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
