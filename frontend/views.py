from django.shortcuts import render

# Create your views here.


def index(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')
def login(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')
def registration(request, *args, **kwargs):
    return render(request, 'frontend/Registration.html')
def homepage(request, *args, **kwargs):
    return render(request, 'frontend/Homepage.html')
def calendar(request, *args, **kwargs):
    return render(request, 'frontend/Calendar.html')
def roomieVal(request, *args, **kwargs):
    return render(request, 'frontend/RoomieVal.html')