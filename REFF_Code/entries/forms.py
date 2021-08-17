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
    
    fact = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Please describe the fact you believe to be accurate",}
        ),
    )
    
    class Meta:
        # Specify which model we're using
        model = Entry

        # Specify the fields we want to use in the form
        fields = (
            'fact',
            'source',
            'category',
        )

class FillEntryModelForm(forms.ModelForm):
    fact = forms.CharField(
        required=True,
        widget=forms.Textarea(),
    )
    
    class Meta:
        # Specify which model we're using
        model = Entry

        # Specify the fields we want to use in the form
        fields = (
            'fact', 'source', 'category'
        )
    

class RequestEntryModelForm(forms.ModelForm):
    fact = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Please describe the fact you'd like to get a source for",}
        ),
    )
    
    class Meta:
        # Specify which model we're using
        model = Entry

        # Specify the fields we want to use in the form
        fields = (
            'fact',
        )

class ReviewModelForm(forms.ModelForm):
    
    
    # Create placeholder text for the comment area of the review
    comment = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Describe how well the source verifies the accuracy of the fact being stated",}
        ),
    )
    
    # The validation below is no longer needed because the validation takes place at the template level for this field
    # add validation for the 'rating' field
    # the format of the validation functions is clean_field_name()
    # def clean_rating(self):
    #     rating = self.cleaned_data['rating']
    #     print('RATING',rating)
        
    #     # # make sure the range is correct
    #     # if rating < 0 or rating > 5:
    #     #     raise ValidationError('Acceptable values only: 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5')
    #     # # make sure the value is a multiple of 0.5
    #     # possible_remainders = []
    #     # for i in range(11):
    #     #     possible_remainders.append(i)
    #     # remainder = rating / 0.5
    #     # if remainder not in possible_remainders:
    #     #     raise ValidationError('Acceptable values only: 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5')
    #     # always return the data
            
    #     return rating
    
    # add validation for the comment field
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 400:
            raise ValidationError('Comment cannot be longer than 400 characters.')
        return comment
    
    def clean(self):
       cleaned_data = super().clean()
       
       # if the user doesn't select a value from 1 to 5, just assign 0 to the rating field
       if 'rating' not in cleaned_data.keys():
           cleaned_data['rating']=0
       return cleaned_data
            

    class Meta:
        model = Review
        fields = ('comment', 'rating', 'expertise')
        help_texts = {'rating': 'Select a value between 0 and 5'}
        


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
