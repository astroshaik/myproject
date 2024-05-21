from django.urls import path
from .views import RoomieView
from .views import TaskView
from .views import RuleView

urlpatterns = [
    path('roomie/', RoomieView.as_view()),
    path('task/', TaskView.as_view()),
    path('rule/', RuleView.as_view()),
    path('home', RoomieView.as_view()), # Make sure this is included
]
