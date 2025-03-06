# tracker/forms.py
from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'time', 'period', 'activity', 'data', 'kcal']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'period': forms.Select(),
            'activity': forms.Select(),
            'data': forms.TextInput(),
            'kcal': forms.NumberInput(attrs={'step': '0.1', 'min': '0'}),
        }

class ImportCSVForm(forms.Form):
    csv_file = forms.FileField(label='Fichier CSV')