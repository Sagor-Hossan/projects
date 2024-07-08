from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = customUser
        fields = ['name', 'username', 'password1', 'password2', 'gender', 'dob', 'about']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class SigninForm(AuthenticationForm):
    class Meta:
        model = customUser
        fields =  ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].help_text = None