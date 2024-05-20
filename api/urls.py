from django.urls import path
from .views import RoomieView

urlpatterns = [
    path('', RoomieView.as_view()),
    path('home', RoomieView.as_view()), # Make sure this is included
]
