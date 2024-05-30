from django.urls import path
from . import views
from .views import add_allergy
from .views import index

urlpatterns = [
    path('', index),
    path('Login', views.login, name='Login'),
    path('Registration', views.registration, name='Registration'),
    path('Homepage', views.homepage, name='Roomie'),
    path('Calendar', views.calendar, name='Calendar'),
    path('RoomieVal', views.RoomieVal, name='RoomieVal'),
    path('logout', views.logout, name='logout'),
    path('add_allergy/', add_allergy, name='add_allergy'),
    path('add_rule', views.add_rule, name='add_rule'),
    path('vote_rule/<int:rule_id>/<str:vote_type>/', views.vote_rule, name='vote_rule'),
    path('delete_allergy/<int:allergy_id>/', views.delete_allergy, name='delete_allergy')
]
