from django.shortcuts import render

# Create your views here.


def index(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')

def regisition_view(request):
    return render(request, 'frontend/Regisition.html')