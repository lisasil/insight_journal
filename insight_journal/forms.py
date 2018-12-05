from django import forms
from .models import Entry
from django.contrib.auth.forms import UserCreationForm

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ('title', 'text',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
