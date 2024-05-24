from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import RegistrationForm
from django.forms import formset_factory
from .forms import RoommateIDForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm, AllergyForm, RuleForm
from api.models import Roomie, Task, Rule, Allergy

def homepage(request):
    roomies = Roomie.object.all()
    tasks = Task.object.all()
    rules = Rule.object.all()
    allergies = Allergy.object.all()
    roomie_data = []

    # Extract tasks, rules, and allergies frome each roomie
    for roomie in roomies:
        roomie_tasks = tasks.filter(roomie=roomie)
        roomie_rules = rules.filter(agreement_roomie_ids__contains=[roomie.roomie_id])
        roomie_allergies = allergies.filter(roomie_ids__contains=[roomie.roomie_id])
    
    roomie_data.append(
        {'roomie': roomie, 'tasks': roomie_tasks, 'rules': roomie_rules, 'allergies': roomie_allergies}
    )

    if request.method == 'POST':
        if 'add_allergy' in request.POST:
            allergy_form = AllergyForm(request.post)
            if allergy_form.is_valid():
                allergy_form.save()
                return redirect('frontend/Homepage.html')
        if 'add_rule' in request.POST:
            rule_form = RuleForm(request.post)
            if rule_form.is_valid():
                rule_form.save()
                return redirect('frontend/Homepage.html')
        else:
            allergy_form = AllergyForm()
            rule_form = RuleForm()

    data = {
        'roomie_data': roomie_data,
        'allergy_form': AllergyForm,
        'rule_form': RuleForm,
    }

    return render(request, "frontend/Homepage.html", data)

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_roomie = form.save()
            # After saving, you can redirect or print form data
            request.session['number_of_roommates'] = form.cleaned_data['number_of_roommates']
            request.session['name'] = form.cleaned_data['name']
            
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
def allergy(request):
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend/HomePage.html')
    else:
        form = AllergyForm()
    return render(request, 'frontend/AddAllergy.html', {'form:': form})

def rule(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend/HomePage.html')
    else:
        form = AllergyForm()
    return render(request, 'frontend/AddRule.html', {'form:': form})

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
