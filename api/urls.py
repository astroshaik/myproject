from django.urls import path
from .views import RoomieView
from .views import TaskView
from .views import RuleView
from .views import RoomieRegistrationView

# Define URL patterns for the Django application. These patterns route HTTP requests to the corresponding views based on the request URL.
urlpatterns = [
    # URL pattern for the RoomieView. This endpoint allows creating a new Roomie.
    # Example usage: POST /roomie/ with Roomie data in request body.
    path('roomie/', RoomieView.as_view()),
    # URL pattern for the TaskView. This endpoint allows creating a new Task.
    # Example usage: POST /task/ with Task data in request body.
    path('task/', TaskView.as_view()),
    # URL pattern for the RuleView. This endpoint allows creating a new Rule.
    # Example usage: POST /rule/ with Rule data in request body.
    path('rule/', RuleView.as_view()),
    # URL pattern for the RoomieRegistrationView. This endpoint handles the registration of new Roomies.
    # It is expected to handle POST requests with data for a new Roomie and return a unique Roomie ID.
    # Example usage: POST /register/ with new Roomie registration data.
    path('register/', RoomieRegistrationView.as_view(), name='roomie-register'),

]
