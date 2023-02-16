from django import forms
from .models import Test

class StartTestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('user',)


