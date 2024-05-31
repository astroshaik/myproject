from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from .forms import RegistrationForm
from django.forms import formset_factory
from .forms import RoommateIDForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from api.models import Roomie
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import jwt
from .forms import LoginForm, AllergyForm, RuleForm
from api.models import Roomie, Task, Rule, Allergy

@require_http_methods(["DELETE"])
def delete_allergy(request, allergy_id):
    try:
        allergy = Allergy.objects.get(id=allergy_id)
        allergy.delete()
        return JsonResponse({'success': True})
    except Allergy.DoesNotExist:
        return JsonResponse({'error': 'Allergy not found'}, status=404)

@require_http_methods(["DELETE"])
def delete_rule(request, rule_id):
    try:
        rule = Rule.objects.get(id=rule_id)
        rule.delete()
        return JsonResponse({'success': True})
    except Rule.DoesNotExist:
        return JsonResponse({'error': 'Rule not found'}, status=404)
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    # Fetch the roomie instance from the database
    try:
        roomie = Roomie.objects.get(email=user.email)
    except Roomie.DoesNotExist:
        roomie = None
    
    # Adding custom data to the token
    if roomie:
        refresh['roomie_id'] = roomie.roomie_id
        refresh['roommate_ids'] = roomie.roommate_ids
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_roomie = form.save()
            new_roomie.roommate_ids = [new_roomie.roomie_id]  # Automatically include self in roommate_ids
            new_roomie.save()
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
            
            if form.cleaned_data['number_of_roommates'] == 0:
                return redirect('http://127.0.0.1:8000/Login')  # Redirect to login or another suitable page
            else:
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
    current_roomie_id = request.session.get('roomie_id')
    try:
        current_roomie = Roomie.objects.get(pk=current_roomie_id)
    except Roomie.DoesNotExist:
        return redirect('login')
    
    number_of_roommates = request.session.get('number_of_roommates', 0)
    RoommateFormSet = formset_factory(RoommateIDForm, extra=int(number_of_roommates))

    if request.method == 'POST':
        formset = RoommateFormSet(request.POST)
        if formset.is_valid():
            roommate_ids = [current_roomie_id]  # Start list with the current user's ID
            for form in formset:
                roommate_id = form.cleaned_data.get('roommate_id')
                if roommate_id:
                    try:
                        potential_roommate = Roomie.objects.get(roomie_id=roommate_id)
                        # Check if the potential roommate's list is empty or contains only zeros
                        if not potential_roommate.roommate_ids or all(r == 0 for r in potential_roommate.roommate_ids):
                            roommate_ids.append(roommate_id)
                        else:
                            form.add_error('roommate_id', f'Roommate ID {roommate_id} already part of a group')
                    except Roomie.DoesNotExist:
                        form.add_error('roommate_id', f'Roommate ID {roommate_id} does not exist')

            # Update roommate IDs for all roommates involved, if no errors
            if not any(formset.errors):
                for rid in roommate_ids:
                    roommate = Roomie.objects.get(roomie_id=rid)
                    roommate.roommate_ids = roommate_ids  # Update all roommate IDs to include each other
                    roommate.save()

                # Send confirmation emails to all roommates
                subject = 'Roommate Validation Completed'
                message = f'Hello, your Roomie validation is complete. Your roommate IDs are: {roommate_ids}.'
                from_email = 'ayeshahussainshaik@gmail.com'
                recipient_list = [roomie.email for roomie in Roomie.objects.filter(roomie_id__in=roommate_ids)]

                send_mail(subject, message, from_email, recipient_list)

                # Redirect to success page or next action
                return redirect('http://127.0.0.1:8000/Login')  # Adjust the redirect URL as needed
            else:
                print("Validation failed due to roommate group conflicts:", formset.errors)
    else:
        formset = RoommateFormSet()

    return render(request, 'frontend/RoomieVal.html', {'formset': formset})

<<<<<<< HEAD


=======
>>>>>>> Ayesha_test
def index(request, *args, **kwargs):
    return redirect('http://127.0.0.1:8000/Login')

def logout(request):
    response = redirect('http://127.0.0.1:8000/Login')  # Redirect to the login page or home page
    response.delete_cookie('jwt')  # Clear the JWT token cookie
    return response

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                roomie = Roomie.objects.get(email=email)
                if roomie.check_password(password):
                    # Token generation
                    payload = {
                        'roomie_id': roomie.roomie_id,
                        'roommate_ids': roomie.roommate_ids,
                        'email': roomie.email,
                        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    
                    response = redirect('http://127.0.0.1:8000/Homepage')
                    response.set_cookie(key='jwt', value=token, httponly=True)  # Set the token in a secure HttpOnly cookie
                    return response
                else:
                    form.add_error(None, 'Invalid email or password')
            except Roomie.DoesNotExist:
                form.add_error(None, 'Invalid email or password')

        return render(request, 'frontend/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'frontend/login.html', {'form': form})
    

def homepage(request, *args, **kwargs):
    # Extract token from cookie
    raw_token = request.COOKIES.get('jwt')
    if not raw_token:
        return JsonResponse({'error': 'No token provided'}, status=401)

    try:
        # Decoding the token
        payload = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=["HS256"])
        roomie_id = payload.get('roomie_id')
        roommate_ids = payload.get('roommate_ids', [])

        # Check if payload contains the necessary data
        if not roomie_id:
            return JsonResponse({'error': 'Token is invalid'}, status=401)

        # Fetch all allergies
        all_allergies = Allergy.objects.all()
        all_rules = Rule.objects.all()
        # Filter allergies manually
        relevant_allergies = [allergy for allergy in all_allergies if any(id in allergy.roomie_ids for id in roommate_ids)]
        official_rules = [rule for rule in all_rules if rule.official and any(id in rule.roommate_ids for id in roommate_ids)]
        tbd_rules = [rule for rule in all_rules if not rule.official and any(id in rule.roommate_ids for id in roommate_ids)]


    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.PyJWTError as e:
        return JsonResponse({'error': str(e)}, status=401)

    # Pass the roomie_id, roommate_ids, and fetched allergies to the template
    context = {
        'roomie_id': roomie_id,
        'roommate_ids': roommate_ids,
        'allergies': relevant_allergies,
        'official_rules': official_rules,
        'tbd_rules': tbd_rules
    }
    return render(request, 'frontend/Homepage.html', context)

def calendar(request, *args, **kwargs):
    return render(request, 'frontend/Calendar.html')

def vote_rule(request, rule_id, vote_type):
    if request.method == 'POST':
        raw_token = request.COOKIES.get('jwt')
        if not raw_token:
            return JsonResponse({'error': 'Authentication'}, status=401)
        
        try:
            payload = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=["HS256"])
            roomie_id = payload.get('roomie_id')

            rule = get_object_or_404(Rule, id=rule_id)

            if vote_type == 'agree':
                print("agree")
                if roomie_id not in rule.agreement_roomie_ids:
                    rule.agreement_roomie_ids.append(roomie_id)
                if roomie_id in rule.disagreement_roomie_ids:
                    rule.disagreement_roomie_ids.remove(roomie_id)
            elif vote_type == 'disagree':
                print("disagree")
                if roomie_id not in rule.disagreement_roomie_ids:
                    rule.disagreement_roomie_ids.append(roomie_id)
                if roomie_id in rule.agreement_roomie_ids:
                    rule.agreement_roomie_ids.remove(roomie_id)
            
            #disagree
            all_roomie_ids = rule.roommate_ids
            print("agreelist")
            print(rule.agreement_roomie_ids)
            print("disagree list")
            print(rule.disagreement_roomie_ids)
            print("roomlist")
            print(rule.roommate_ids)
            if set(rule.disagreement_roomie_ids) == set(all_roomie_ids):
                rule.delete()
            elif set(rule.agreement_roomie_ids) == set(all_roomie_ids):
                print("official")
                rule.official = True
                rule.save()
            else:
                rule.official = False
                rule.save()
            
            return redirect('http://127.0.0.1:8000/Homepage')
        except jwt.PyJWTError as e:
            return JsonResponse({'error': str(e)}, status=401)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
def add_rule(request): 
    if request.method == 'POST':
        raw_token = request.COOKIES.get('jwt')
        if not raw_token:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            payload = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=["HS256"])
            roomie_id = payload.get('roomie_id')

            rule_name = request.POST.get('rule_name')
            rule_description = request.POST.get('rule_description')
            agreement_roomie_ids=[]
            agreement_roomie_ids.append(roomie_id)
            roommate_ids= payload.get('roommate_ids', [])
            
            disagreement_roomie_ids = list(roommate_ids)
            disagreement_roomie_ids.remove(roomie_id)
            print(disagreement_roomie_ids)
            print(roommate_ids)

            new_rule = Rule(
                title=rule_name,
                description=rule_description,
                agreement_roomie_ids=agreement_roomie_ids,
                disagreement_roomie_ids=disagreement_roomie_ids,
                official=False,
                roommate_ids = roommate_ids,
            )
            new_rule.save()
            return redirect('http://127.0.0.1:8000/Homepage')  # Redirect back to homepage
        except jwt.PyJWTError as e:
            return JsonResponse({'error': str(e)}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
  
def add_allergy(request):
    if request.method == 'POST':
        raw_token = request.COOKIES.get('jwt')
        if not raw_token:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            payload = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=["HS256"])
            roomie_id = payload.get('roomie_id')
            roommate_ids = payload.get('roommate_ids')

            allergy_name = request.POST.get('allergy_name')
            allergy_description = request.POST.get('allergy_description')

            new_allergy = Allergy(
                name=allergy_name,
                description=allergy_description,
                roomie_ids=roommate_ids  # Assuming roomie_ids includes the roomie itself and their roommates
            )
            new_allergy.save()
            return redirect('http://127.0.0.1:8000/Homepage')  # Redirect back to homepage or another appropriate view
        except jwt.PyJWTError as e:
            return JsonResponse({'error': str(e)}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt')
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.roomie = Roomie.objects.get(roomie_id=payload['roomie_id'])
            except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError, Roomie.DoesNotExist):
                response = JsonResponse({'error': 'Authentication failed'}, status=401)
                response.delete_cookie('jwt')
                return response