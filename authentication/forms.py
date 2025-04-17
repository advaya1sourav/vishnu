from django import forms
from users.models import Volunteer
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    city = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Volunteer
        fields = ['username', 'email', 'dob', 'city', 'password1', 'password2']