from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import RegistrationForm
from django.forms import formset_factory
from .forms import RoommateIDForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from api.models import Roomie


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_roomie = form.save()
            # After saving, you can redirect or print form data
            request.session['number_of_roommates'] = form.cleaned_data['number_of_roommates']
            request.session['name'] = form.cleaned_data['name']
            request.session['roomie_id'] = new_roomie.roomie_id
            
            # Prepare and send the email
            subject = 'Welcome, new Roomie!'
            message = f'Hello {form.cleaned_data["name"]}, you have been registered with Roomie ID: {new_roomie.roomie_id}.'
            from_email = 'ayeshahussainshaik@gmail.com'
            recipient_list = [form.cleaned_data['email']]
            
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('http://127.0.0.1:8000/RoomieVal')

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
    current_roomie_id = request.session.get('roomie_id')  # Assumes a logged-in Roomie ID is stored in session

    try:
        current_roomie = Roomie.objects.get(pk=current_roomie_id)
    except Roomie.DoesNotExist:
        return redirect('login') 
    number_of_roommates = request.session.get('number_of_roommates', 0)
    print("numroom data:", number_of_roommates)

    # Create a formset with the correct number of extra forms
    RoommateFormSet = formset_factory(RoommateIDForm, extra=int(number_of_roommates))

    if request.method == 'POST':
        formset = RoommateFormSet(request.POST)
        if formset.is_valid():
            new_roommate_ids = []
            for form in formset:
                roommate_id = form.cleaned_data.get('roommate_id')
                try:
                    roommate = Roomie.objects.get(roomie_id=roommate_id)
                    # Update roommate_ids for both current roomie and the found roommate
                    if current_roomie_id not in roommate.roommate_ids:
                        roommate.roommate_ids.append(current_roomie_id)
                        roommate.save()
                    if roommate_id not in current_roomie.roommate_ids:
                        current_roomie.roommate_ids.append(roommate.roommate_ids)
                except Roomie.DoesNotExist:
                    form.add_error('roommate_id', f'Roommate ID {roommate_id} does not exist')

            # Update the current Roomie's roommate_ids field
            current_roomie.roommate_ids = new_roommate_ids
            current_roomie.save()
            return render(request, 'frontend/Login.html')  # Redirect to a success or next action page
    else:
        formset = RoommateFormSet()  # Generate the formset with the required number of forms

    return render(request, 'frontend/RoomieVal.html', {'formset': formset})

# Create your views here.


def index(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')

def login(request, *args, **kwargs):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print("Form pass:", password)
            print("Form email:", email)
            try:
                roomie = Roomie.objects.get(email=email)
                if roomie.check_password(password):
                    # Assume you have a way to handle login sessions
                    request.session['roomie_id'] = roomie.roomie_id
                    return redirect('http://127.0.0.1:8000/Login')  # Redirect to a success page
                else:
                    form.add_error(None, 'Invalid credentials')
            except Roomie.DoesNotExist:
                form.add_error(None, 'Invalid credentials')
  # Add non-field error
    else:
        form = LoginForm()

    return render(request, 'frontend/login.html', {'form': form})

def homepage(request, *args, **kwargs):
    return render(request, 'frontend/Homepage.html')
def calendar(request, *args, **kwargs):
    return render(request, 'frontend/Calendar.html')
