from django import forms
from .models import Ticket
from django.contrib.auth.forms import AuthenticationForm

class TicketForm(forms.ModelForm):
    subject = forms.CharField(required=False)
    class Meta:
        model = Ticket
        fields = ['name', 'subject', 'message']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)