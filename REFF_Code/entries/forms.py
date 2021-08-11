# We use this file to create forms

from django import forms
from django.core.exceptions import ValidationError
from entries.models import Entry, Review
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
            'category',
        )


class ReviewModelForm(forms.ModelForm):
    # add validation for the 'rating' field

    # the format of the validation functions is clean_field_name()
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise ValidationError('The rating value can only be one of these: 0 1 2 3 4 5')
        # always return the data
        return rating

    class Meta:
        model = Review
        fields = ('comment', 'rating',)


# The below form is the more comprehensive way of using forms in Django;
# It is good for understanding the behind the scenes workings.


class EntryForm(forms.Form):

    fact = forms.CharField()
    source = forms.URLField()
    category = forms.CharField(max_length=100)

# Create a custom user creation form where we use our own type of 'user' as opposed to Django's default one


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        field_classes = {'username': UsernameField}
