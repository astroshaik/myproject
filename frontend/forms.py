# frontend/forms.py
from django import forms
from api.models import Roomie

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Roomie
        fields = ['email', 'password','name', 'number_of_roommates', 'roommate_ids']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
