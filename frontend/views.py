from django.shortcuts import render
# frontend/views.py
from .forms import RegistrationForm

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'frontend/Login.html') # Redirect to login after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'frontend/Registration.html', {'form': form})

# Create your views here.


def index(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')
def login(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')

def homepage(request, *args, **kwargs):
    return render(request, 'frontend/Homepage.html')
def calendar(request, *args, **kwargs):
    return render(request, 'frontend/Calendar.html')
def roomieVal(request, *args, **kwargs):
    return render(request, 'frontend/RoomieVal.html')