from django.urls import path
from .views import RoomieView
from .views import TaskView
from .views import RuleView
from .views import RoomieRegistrationView


urlpatterns = [
    path('roomie/', RoomieView.as_view()),
    path('task/', TaskView.as_view()),
    path('rule/', RuleView.as_view()),
    path('register/', RoomieRegistrationView.as_view(), name='roomie-register'),

]
