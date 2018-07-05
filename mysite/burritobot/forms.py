from django import forms
from .models import Command

CommandFormSet = forms.modelformset_factory(Command, fields=('command', 'response'))
