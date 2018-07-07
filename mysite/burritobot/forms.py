from django import forms
from .models import Command

CommandFormSet = forms.modelformset_factory(Command, fields=('command', 'response', 'user'), can_delete=True)

class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['command', 'response']