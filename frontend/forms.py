# frontend/forms.py
from django import forms
from api.models import Roomie, Allergy, Rule
from django.contrib.auth.hashers import make_password  # Import make_password for hashing
from api.models import Roomie
from django.contrib.auth.hashers import make_password 

# Import make_password for hashing


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Roomie
        fields = ['email', 'password', 'name', 'number_of_roommates']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # Hash password before saving
        if commit:
            user.save()
        return user
class RoommateIDForm(forms.Form):
    roommate_id = forms.IntegerField(label='Roommate ID')
    
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['name', 'description']

class RuleForm(forms.ModelForm):
    
    class Meta:
        model = Rule
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    #roommate_ids = forms.ModelMultipleChoiceField(queryset=Roomie.objects.none(), widget=forms.SelectMultiple)
    class Meta:
        model = Task
        fields = ['tasks', 'start_time', 'end_time', 'task_type', 'roommate_ids']
