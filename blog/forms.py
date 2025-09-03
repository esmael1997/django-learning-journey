from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    subject = forms.CharField(required=False)
    class Meta:
        model = Ticket
        fields = ['name', 'subject', 'message']
