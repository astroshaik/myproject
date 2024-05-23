from django.shortcuts import render, redirect
# frontend/views.py
from .forms import RegistrationForm
from django.forms import formset_factory
from .forms import RoommateIDForm



def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_roomie = form.save()
            # After saving, you can redirect or print form data
            request.session['number_of_roommates'] = form.cleaned_data['number_of_roommates']

            print("Form data:", form.data) 
            return redirect('http://127.0.0.1:8000/RoomieVal') # Redirect to login after successful registration
        else:
            form = RegistrationForm()
            print("Form data not valide:", form.errors)
            return render(request, 'frontend/Registration.html', {'form': form})
    else:
        form = RegistrationForm()
        print("Form data:", form.data)
    return render(request, 'frontend/Registration.html', {'form': form})

def RoomieVal(request):
    # Assume number_of_roommates is fetched from the session or user model
    number_of_roommates = request.session.get('number_of_roommates', 0)
    print("numroom data:", number_of_roommates)

    # Create a formset with the correct number of extra forms
    RoommateFormSet = formset_factory(RoommateIDForm, extra=int(number_of_roommates))

    if request.method == 'POST':
        formset = RoommateFormSet(request.POST)
        if formset.is_valid():
            # handle the cleaned data
            return redirect('http://127.0.0.1:8000/Login')  # Redirect or handle next step
    else:
        formset = RoommateFormSet()  # Generate the formset with the required number of forms

    return render(request, 'frontend/RoomieVal.html', {'formset': formset})

# Create your views here.


def index(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')
def login(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')

def homepage(request, *args, **kwargs):
    return render(request, 'frontend/Homepage.html')
def calendar(request, *args, **kwargs):
    return render(request, 'frontend/Calendar.html')
