from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from entries.models import Entry
from entries.forms import EntryForm, EntryModelForm, CustomUserCreationForm
# folder contains TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
# we'll use this class to verify that the current user is authenticated
from django.contrib.auth.mixins import LoginRequiredMixin

# Generally speaking, web pages follow the CRUD+L format: Create, Retrieve, Updated, Delete and List

# Class view


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

# Class view


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

# Function view


def landing_page(request):
    return render(request, "landing.html")


# Class view
# By also inheritting from LoginRequiredMixin, we restrict access to this particular view (it can only be called when the user is logged in)
class EntryListView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"
    queryset = Entry.objects.all()
    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

# Class View
class EntryListByCategoryView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"
    
    def get_queryset(self):
        category=self.kwargs['category']
        return Entry.objects.filter(category=category)
    
    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"
    
# Class View
class MyEntryListByCategoryView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"
    
    def get_queryset(self):
        entry_user = self.request.user
        category=self.kwargs['category']
        return Entry.objects.filter(user=entry_user,category=category)
    
    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

# Function view
def entry_list(request):
    entries = Entry.objects.all()
    context = {
        "entries": entries
    }
    return render(request, "entries/entry_list.html", context)


class MyEntryListView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"

    # Filter the query set so we only display the entries of the current user
    def get_queryset(self):
        entry_user = self.request.user
        return Entry.objects.filter(user=entry_user)
    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

# Class view
# We won't restrict this view from being accessed by non-users because we want it to be accessible across the web


class EntryDetailView(generic.DetailView):
    template_name = "entries/entry_detail.html"
    queryset = Entry.objects.all()
    context_object_name = "entry"

# Function view


def entry_detail(request, pk):
    # Return the entry with id = pk
    entry = Entry.objects.get(id=pk)
    context = {
        "entry": entry
    }
    return render(request, "entries/entry_detail.html", context)

# Class view


class EntryCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "entries/entry_create.html"
    form_class = EntryModelForm

    def get_success_url(self):
        return reverse("entries:entry-list")

    def form_valid(self, form):
        # Assign the current logged in user to the entry
        entry = form.save(commit=False)
        entry.user = self.request.user
        entry.save()

        send_mail(
            subject="New entry has been created",
            message="Thanks for contributing to the REFF database.",
            from_email="test@test.com",
            recipient_list=[entry.user.email],
        )
        return super(EntryCreateView, self).form_valid(form)

# Function view


def entry_create(request):
    # Generate empty form
    form = EntryModelForm()
    # If the request is of type 'POST'
    if request.method == "POST":
        print('Receiving a post request.')
        form = EntryModelForm(request.POST)
        # Check to see that the form is valid
        if form.is_valid():
            # The following method simply saves the form as an instance in the database
            form.save()
            return redirect("/entries")

    context = {
        "form": form
    }

    return render(request, "entries/entry_create.html", context)

# Class view


class EntryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "entries/entry_update.html"
    queryset = Entry.objects.all()
    form_class = EntryModelForm

    def get_success_url(self):
        return reverse("entries:entry-list")

# Function view


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


# Class view
class EntryDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "entries/entry_delete.html"
    queryset = Entry.objects.all()

    def get_success_url(self):
        return reverse("entries:entry-list")

# Function view


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
