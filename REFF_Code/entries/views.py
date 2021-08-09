from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from entries.models import Entry
from entries.forms import EntryForm, EntryModelForm, CustomUserCreationForm
# folder contains TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
# we'll use this class to verify that the current user is authenticated
from django.contrib.auth.mixins import LoginRequiredMixin

# Use custom url_generator to assign to each new entry
from algorithms.random_url_string import url_generator

# We'll use these classes to paginate a higher number of entries that are to be displayed
from django.core.paginator import Paginator, EmptyPage

import json

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

# Class view


class TestingView(generic.TemplateView):
    template_name = "entries/testing.html"

# Function view


def landing_page(request):
    return render(request, "landing.html")


# Class view
# By also inheritting from LoginRequiredMixin, we restrict access to this particular view (it can only be called when the user is logged in)
class EntryListView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/testing_2.html"
    # Declare the number of entries per page
    paginate_by = 10
    # # Order entries by date_created (the '-' means last added first)
    # queryset = Entry.objects.all().order_by('-date_created')
    
    def get_queryset(self):
        # print(self.request.GET)
        # Order entries by date_created (the '-' means last added first)
        entries = Entry.objects.all().order_by('-date_created')
        if 'category' in self.request.GET.keys():
            category=self.request.GET['category']
            # if the category is different to 'all' apply another filter to the entries
            if (category!='all'):
                entries = entries.filter(category=category)
        # Filter the queryset in order to display entries created by the user logged in
        if 'by_me' in self.request.GET.keys():
            by_me=self.request.GET['by_me']
            if by_me=='true':
                entry_user = self.request.user
                entries=entries.filter(user=entry_user)
            
        return entries
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # default value for category
        category = 'all'
        # grab the 'category' parameter from the URL of form "/?category=xXxX"
        if 'category' in self.request.GET.keys():
            category = self.request.GET['category']
        # add category to context
        context['category']=category
        # add number of entries to context
        context["num_entries"] = len(self.get_queryset())
        print(self.request.GET)
        # print('LENGTH ' + str(len(self.get_queryset())))
        # default value for by_me is 'false'
        by_me='false'
        if 'by_me' in self.request.GET.keys() and self.request.GET['by_me']=='true':
            by_me='true'
            
        context['by_me']=by_me
        
        return context
    


# Class View

class EntryListByCategoryView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/testing.html"

    def get_queryset(self):
        category = self.kwargs['category']
        return Entry.objects.filter(category=category)

    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

# Class View


class MyEntryListByCategoryView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"

    def get_queryset(self):
        entry_user = self.request.user
        category = self.kwargs['category']
        return Entry.objects.filter(user=entry_user, category=category)

    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

# Function view


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

# Class view


class EntryDetailShortURLView(generic.DetailView):
    template_name = "entries/entry_detail.html"

    # return the Entry which has the corresponding short URL
    def get_object(self, queryset=None):
        short_url = self.kwargs['short_url']
        entry = Entry.objects.get(short_url=short_url)
        return entry

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
        # Generate random short URL
        random_short_url = url_generator()
        # Check if the random short URL already exists in the DB for another entry
        identical_urls = Entry.objects.filter(
            short_url=random_short_url).count()
        # print('>>>>> Number of idential short URLs =',identical_urls)
        # If it already exists, re-generate it
        if(identical_urls > 0):
            random_short_url = url_generator()
        # Assign short URL to the new entry
        entry.short_url = random_short_url
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

#######################
### DEPRECATED CODE ###
#######################

# Function view

def entry_list(request):
    # Order entries by date_created (the '-' means last added first)
    entries = Entry.objects.all().order_by('-date_created')
    # default value of 'category'
    category = 'all'
    print(request.GET.keys())
    
    # if 'category' is passed as a '?category=xXx' parameter to the URL
    if 'category' in request.GET.keys():
        category=request.GET['category']
        # if the category is different to 'all' apply another filter to the entries
        if (category!='all'):
            entries = entries.filter(category=category)
    
    # Create the paginator, and define the number of entries per page
    p = Paginator(entries, 4)
    num_pages = p.num_pages
    
    # get the page_num from the request;
    # if the request dictionary does not contain 'page', use page 1 as default
    page_num = request.GET.get('page', 1)
    
    # print('Current page: ', page_num)
    # print('Total number of pages: ',p.num_pages)
    # print('Number of entries: ',len(entries))
    

    # if a user tries to access a page that doesn't exist, take them to page 1;
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    entry_number = len(entries)
    print(entry_number)
    
    context = {
        "entries": page,
        "num_pages": num_pages,
        "page_num": page_num,
        "entry_number": entry_number,
        "category": category
    }
    return render(request, "entries/testing.html", context)


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
