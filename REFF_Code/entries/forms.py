# We use this file to create forms

from django import forms
from entries.models import Entry

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
            'user',
        )


# The below form is the more comprehensive way of using forms in Django;
# It is good for understanding the behind the scenes workings.
class EntryForm(forms.Form):

    fact = forms.CharField()
    source = forms.URLField()
    credibility = forms.FloatField()
    category = forms.CharField(max_length=100)


