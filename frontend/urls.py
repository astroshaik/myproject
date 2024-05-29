from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('', index),
    path('Login', views.login, name='Login'),
    path('Registration', views.registration, name='Registration'),
    path('Homepage', views.homepage, name='Roomie'),
    path('Calendar', views.calendar, name='Calendar'),
    #path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('RoomieVal', views.RoomieVal, name='RoomieVal'),
    path('logout', views.logout, name='logout'),
]
