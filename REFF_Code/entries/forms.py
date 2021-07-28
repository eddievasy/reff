# We use this file to create forms

from django import forms
from entries.models import Entry
from django.contrib.auth.forms import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

# Specify user
User = get_user_model()

# The following is a more compact way of using forms within Django


class EntryModelForm(forms.ModelForm):
    class Meta:
        # Specify which model we're using
        model = Entry
        
        # Specify the fields we want to use in the form
        fields = (
            'fact',
            'source',
            'credibility',
            'category',
            'user'
        )
        

# The below form is the more comprehensive way of using forms in Django;
# It is good for understanding the behind the scenes workings.


class EntryForm(forms.Form):

    fact = forms.CharField()
    source = forms.URLField()
    credibility = forms.FloatField()
    category = forms.CharField(max_length=100)

# Create a custom user creation form where we use our own type of 'user' as opposed to Django's default one


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        field_classes = {'username': UsernameField}
