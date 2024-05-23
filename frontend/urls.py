from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.index, name='Login'),
    path('regisition/', views.regisition_view, name='Regisition'),
]
