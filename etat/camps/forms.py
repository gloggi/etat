
from django import forms

import models

class CampForm(forms.ModelForm):
    class Meta:
        model = models.Camp
        fields = (
            'title',
            'type',
            'department',
            'begin',
            'end',
            'min_birth_year',
            'fee',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-lg'}),
            'begin': forms.DateInput(attrs={'class': 'datepicker'}),
            'end': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        exclude = ('member', 'camp', 'confirmation')
        widgets = {
            'signup_date': forms.DateInput(attrs={'class': 'date'}),
            'payed_date': forms.DateInput(attrs={'class': 'date'}),
            'payed_fee': forms.TextInput,
        }

