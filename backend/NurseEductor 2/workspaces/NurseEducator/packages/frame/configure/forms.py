from django import forms

from .models import FramesModel

class FramesModelForm(forms.ModelForm):
    
    class Meta:
        model = FramesModel
        # fields = '__all__'
        fields = ['user_role', 'config']

