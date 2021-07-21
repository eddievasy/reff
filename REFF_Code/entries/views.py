from django.shortcuts import render, redirect
from django.http import HttpResponse
from entries.models import Entry, Contributor
from entries.forms import EntryForm, EntryModelForm

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
    form = EntryModelForm()
    # If the request is of type 'POST'
    if request.method=="POST":
        print('Receiving a post request.')
        form = EntryModelForm(request.POST)
        # Check to see that the form is valid
        if form.is_valid():
            # The following method simply saves the form as an instance in the database
            form.save()
            return redirect("/entries")

    context= {
        "form": form
    }

    return render(request, "entries/entry_create.html", context)


def entry_update(request, pk):
    entry = Entry.objects.get(id=pk)
    form = EntryModelForm(instance=entry)
    if request.method == "POST":
        form = EntryModelForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("/entries")
     
    context = {
        "form": form,
        "entry": entry
    }

    return render(request, "entries/entry_update.html", context)

def entry_delete(request, pk):
    entry = Entry.objects.get(id=pk)
    entry.delete()
    return redirect("/entries")

# Below we've got the form using the EntryForm as opposed to EntryModelForm
# However, this version is lengthier. The one above abstracts more code.

# def entry_create(request):
    # # Generate empty form
    # form = EntryForm()
    # # If the request is of type 'POST'
    # if request.method=="POST":
    #     print('Receiving a post request.')
    #     form = EntryForm(request.POST)
    #     # Check to see that the form is valid
    #     if form.is_valid():
    #         print("The form is valid.")
    #         print(form.cleaned_data)

    #         fact = form.cleaned_data['fact']
    #         source = form.cleaned_data['source']
    #         credibility = form.cleaned_data['credibility']
    #         category = form.cleaned_data['category']

    #         contributor = Contributor.objects.first()

    #         Entry.objects.create(
    #             fact=fact,
    #             source=source,
    #             credibility=credibility,
    #             category=category,
    #             user=contributor
    #         )

    #         # Return to the entries page after the new entry has been created
    #         print('New entry has been created.')
    #         return redirect("/entries")

    # context= {
    #     "form": form
    # }

#     return render(request, "entries/entry_create.html", context)