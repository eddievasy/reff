from django.shortcuts import render
from django.http import HttpResponse
from entries.models import Entry, Contributor
from entries.forms import EntryForm

# Create your views here.
 
def entry_list(request):
    entries = Entry.objects.all()
    context = {
        "entries": entries
    }
    return render(request, "entries/entry_list.html", context)

def entry_detail(request, pk):
    # Return the entry with id = pk
    entry = Entry.objects.get(id=pk)
    context = {
        "entry": entry
    }
    return render(request, "entries/entry_detail.html", context)

def entry_create(request):
    # Generate empty form
    form = EntryForm()
    # If the request is of type 'POST'
    if request.method=="POST":
        print('Receiving a post request.')
        form = EntryForm(request.POST)
        # Check to see that the form is valid
        if form.is_valid():
            print("The form is valid.")
            print(form.cleaned_data)

            fact = form.cleaned_data['fact']
            source = form.cleaned_data['source']
            credibility = form.cleaned_data['credibility']
            category = form.cleaned_data['category']

            contributor = Contributor.objects.first()

            Entry.objects.create(
                fact=fact,
                source=source,
                credibility=credibility,
                category=category,
                user=contributor
            )

            print('New entry has been created.')

    context= {
        "form": form
    }
    return render(request, "entries/entry_create.html", context)