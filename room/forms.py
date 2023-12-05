from django import forms
from .models import RoomReservation, Calendar
from login.models import UserProfile

# class RoomReservationForm(forms.ModelForm):
#     class Meta:
#         model = RoomReservation
#         fields = ['student', 'room', 'start_time', 'end_time']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')
#
#         # Your custom validation logic here
#
#         return cleaned_data
class RoomReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['student', 'room', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)

        super(RoomReservationForm, self).__init__(*args, **kwargs)

        if user_id:
            self.fields['student'].queryset = UserProfile.objects.filter(id=user_id)
        else:
            self.fields['student'].queryset = UserProfile.objects.all()

    def save(self, commit=True):
        instance = super(RoomReservationForm, self).save(commit=False)
        if commit:
            print("UserProfile instance in save method:", self.cleaned_data['student'])
            user_profile = self.cleaned_data['student']
            instance.student = user_profile
            instance.save()
        return instance



class CalendarEditForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['title', 'start', 'end', 'allDay']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
