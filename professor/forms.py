from django import forms
from .models import Calendar


class CalendarEditForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['title', 'start', 'end', 'allDay']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
