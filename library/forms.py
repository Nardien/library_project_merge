from django import forms
from library.models import *
from django.forms import ModelForm

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

class Form(ModelForm):
	class Meta:
		model=Search
		fields=['name']
