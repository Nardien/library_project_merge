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


class RequestForm(forms.Form) :
    book_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'title': 'Book Name',
                'class': 'form-control',
            }
        )
    )
    author = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'title': 'Author Name',
                'class': 'form-control',
            }
        )
    )
    genre = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices = (('phi', 'phi'), ('soc', 'soc'), ('nat', 'nat'), ('eng', 'eng'), ('lan', 'lan'))
    )

class SeminarForm(forms.Form) :
    borrow_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            attrs={
                'class': 'form-control'
            }
        )
    )
