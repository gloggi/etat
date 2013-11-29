
from django import forms
from django.forms.models import inlineformset_factory

import models

class CampForm(forms.ModelForm):
    class Meta:
        model = models.Camp
        exclude = ('members',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-lg'}),
            'begin': forms.DateInput(attrs={'class': 'date'}),
            'end': forms.DateInput(attrs={'class': 'date'}),
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

