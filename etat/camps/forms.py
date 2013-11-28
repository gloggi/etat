
from django import forms
from django.forms.models import inlineformset_factory

import models

class CampForm(forms.ModelForm):
    class Meta:
        model = models.Camp
        exclude = ('participants',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-lg'}),
            'begin': forms.DateInput(attrs={'class': 'datepicker'}),
            'end': forms.DateInput(attrs={'class': 'datepicker'}),
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ('type', 'signup_date', 'payed_fee', 'payed_date')
        widgets = {
            'signup_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'payed_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'payed_fee': forms.TextInput,
        }

ParticipantsFormset = inlineformset_factory(
    models.Camp,
    models.Participant,
    form=ParticipantForm,
    extra=0,
)