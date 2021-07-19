# We use this file to create forms

from django import forms

class EntryForm(forms.Form):
    CATEGORY = (
        ('Technology','Technology'),
        ('Nutrition','Nutrition'),
        ('Politics','Politics')
        # To add more
    )

    fact = forms.CharField()
    source = forms.URLField()
    credibility = forms.FloatField()
    category = forms.CharField(max_length=100)


