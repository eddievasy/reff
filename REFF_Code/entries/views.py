from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from entries.models import Entry, Review, User, Like
from entries.forms import EntryForm, EntryModelForm, CustomUserCreationForm, ReviewModelForm, RequestEntryModelForm, FillEntryModelForm
# folder contains TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
# we'll use this class to verify that the current user is authenticated
from django.contrib.auth.mixins import LoginRequiredMixin

# Use custom url_generator to assign to each new entry
from algorithms.random_url_string import url_generator

# Use domain_extractor to extract the domain from the long URL source
from algorithms.domain_extractor import url_parser

# We'll use these classes to paginate a higher number of entries that are to be displayed
from django.core.paginator import Paginator, EmptyPage

# we need to use Avg to calculate the average scores
from django.db.models import Avg

# use this method for passing the current date and time when filling a request-type entry
from datetime import datetime

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # get all relevant data from DB to pass onto the context
        num_entries = Entry.objects.count()
        num_users = User.objects.count()
        num_reviews = Review.objects.count()
        num_likes = Like.objects.count()
        
        # add data to context
        context['num_entries']=num_entries
        context['num_users']=num_users
        context['num_reviews']=num_reviews
        context['num_likes']=num_likes
        
        print(context)
        return context

# Class view


class TestingView(generic.TemplateView):
    template_name = "entries/testing.html"


# Class view
# By also inheritting from LoginRequiredMixin, we restrict access to this particular view (it can only be called when the user is logged in)
class EntryListView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"
    # Declare the number of entries per page
    paginate_by = 10
    # # Order entries by date_created (the '-' means last added first)
    # queryset = Entry.objects.all().order_by('-date_created')

    def get_queryset(self):
        # print(self.request.GET)
        # Order entries by date_created (the '-' means last added first)
        entries = Entry.objects.all().order_by('-date_created')
        if 'category' in self.request.GET.keys():
            category = self.request.GET['category']
            # if the category is different to 'all' apply another filter to the entries
            if (category != 'all'):
                entries = entries.filter(category=category)
        # Filter the queryset in order to display entries created by the user logged in
        if 'by_me' in self.request.GET.keys():
            by_me = self.request.GET['by_me']
            if by_me == 'true':
                entry_user = self.request.user
                entries = entries.filter(user=entry_user)
                # print(entries)
        
        if 'likes' in self.request.GET.keys():
            likes = self.request.GET['likes']
            if likes == 'true':
                entry_user = self.request.user
                # fetch all the likes of the currently logged in user
                likes = Like.objects.filter(user=entry_user)
                entry_id_list = list()
                # save the entry id's corresponding to each like in a list
                for like in likes:
                    entry_id_list.append(like.entry_id)
                # print(entry_id_list)
                # filter the entries to only contain the ones liked by the user
                entries=entries.filter(id__in=entry_id_list)
                # print(entries)
                

        # if the search function is being used, further filter the queryset
        if 'search' in self.request.GET.keys():
            search_keyword = self.request.GET['search']
            entries = entries.filter(fact__contains=search_keyword)

        # make sure only the full entries are included (not the request-type entries)
        entries = entries.filter(normal_entry=True)

        return entries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # default value for category
        category = 'all'
        # grab the 'category' parameter from the URL of form "/?category=xXxX"
        if 'category' in self.request.GET.keys():
            category = self.request.GET['category']
        # add category to context
        context['category'] = category
        # add number of entries to context
        context["num_entries"] = len(self.get_queryset())
        # print(self.request.GET)
        # print('LENGTH ' + str(len(self.get_queryset())))
        # default value for parameter 'by_me' is 'false'
        by_me = 'false'
        if 'by_me' in self.request.GET.keys() and self.request.GET['by_me'] == 'true':
            by_me = 'true'
        context['by_me'] = by_me
        
        # default value for parameter 'likes' is 'false'    
        likes = 'false'
        if 'likes' in self.request.GET.keys() and self.request.GET['likes'] == 'true':
            likes = 'true'
        context['likes'] = likes
        

        additional_info = {}

        # add an 'additional_info' dictionary to the context in which we will store the domain urls to display in the template
        object_list = context['object_list']
        for object in object_list:
            domain_url = url_parser(object.source)
            additional_info[object.id] = domain_url

        context['additional_info'] = additional_info

        # add an 'additional_info_2' dictionary to the context in which we will store the average scores for each entry we iterate over in the template
        additional_info_2 = {}
        for object in object_list:
            # returns a dictionary with the key 'rating__avg'
            score = Review.objects.filter(
                entry=object).aggregate(Avg('rating'))
            # returns the actual average score value
            average_score = score['rating__avg']
            # print(average_score)

            # round all float instances to 1 decimal, and replace all NoneType with 0
            if isinstance(average_score, float):
                average_score = round(average_score, 1)
                # print(average_score)
            else:
                average_score = 0
            additional_info_2[object.id] = average_score

        context['additional_info_2'] = additional_info_2

        # print('CONTEXT --->', context)
        print()

        return context


# Class view
class ReviewListView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/review_list.html"
    # Declare the number of entries per page
    paginate_by = 10

    def get_queryset(self):
        # Get the entry id of the entry we want to see the reviews for
        entry_id = self.request.GET['id']

        # check to see if there is a 'search' parameter in the URL
        if 'search' in self.request.GET.keys():
            # fetch all reviews for that specific entry_id which contain the search parameter
            reviews = Review.objects.filter(entry_id=entry_id)
            search_keyword = self.request.GET['search']
            reviews = reviews.filter(comment__contains=search_keyword)
        else:
            # fetch all reviews for that specific entry_id
            reviews = Review.objects.filter(entry_id=entry_id)

        # order all reviews to show the last ones created first
        reviews = reviews.order_by('-date_created')

        return reviews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get the object_list in order to generate a new dictionary which contains user names
        object_list = context['object_list']
        # use this dictionary to store user names
        additional_info = {}

        # for each review id, attach a value corresponding to the username of the user that left the review
        for object in object_list:
            user_id = object.user_id
            username = User.objects.get(id=user_id).username
            additional_info[object.id] = username

        # add dictionary to the context so we can use it in the template
        context['additional_info'] = additional_info

        # Get the entry id of the entry we want to see the reviews for
        entry_id = self.request.GET['id']
        entry_short_url = Entry.objects.get(id=entry_id).short_url
        # add entry_short_url to context
        context['entry_short_url'] = entry_short_url
        # add entry_id to context
        context['entry_id'] = entry_id

        # add the number of reviews to the context
        context["num_reviews"] = len(self.get_queryset())

        # print(context)

        return context

# Class view
# We won't restrict this view from being accessed by non-users because we want it to be accessible across the web


class EntryDetailView(generic.DetailView):
    template_name = "entries/entry_detail.html"
    queryset = Entry.objects.all()
    context_object_name = "entry"

# Class view

# class LikeEntryView(generic.DetailView):
#     template_name = "entries/entry_detail.html"

#     # return the Entry which has the corresponding short URL

#     def get_object(self, queryset=None):
#         short_url = self.kwargs['short_url']
#         entry = Entry.objects.get(short_url=short_url)
#         return entry

#     # pass the source_domain through the context to the HTML template
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         entry = self.get_object()
#         context['source_domain'] = url_parser(entry.source)
#         # print(context)

#         # Add 'average_score' to context
#         # returns a dictionary with the key 'rating__avg'
#         score = Review.objects.filter(
#             entry=entry).aggregate(Avg('rating'))
#         # returns the actual average score value
#         average_score = score['rating__avg']
#         # print(average_score)
#         # round all float instances to 1 decimal, and replace all NoneType with 0
#         if isinstance(average_score, float):
#             average_score = round(average_score, 1)
#             # print(average_score)
#         else:
#             average_score = 0
#         context['average_score'] = average_score

#         # Add 'reviews_number' to context
#         # print(Review.objects.filter(entry=entry))
#         reviews_number = len(Review.objects.filter(entry=entry))
#         # print(reviews_number)
#         context['reviews_number'] = reviews_number

#         print(context)

#         return context

#     context_object_name = "entry"

# Class view


class EntryDetailShortURLView(generic.DetailView):
    template_name = "entries/entry_detail.html"

    # return the Entry which has the corresponding short URL

    def get_object(self, queryset=None):
        short_url = self.kwargs['short_url']
        entry = Entry.objects.get(short_url=short_url)
        return entry

    # pass the source_domain through the context to the HTML template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.get_object()
        context['source_domain'] = url_parser(entry.source)
        # print(context)

        # Add 'average_score' to context
        # returns a dictionary with the key 'rating__avg'
        score = Review.objects.filter(
            entry=entry).aggregate(Avg('rating'))
        # returns the actual average score value
        average_score = score['rating__avg']
        # print(average_score)
        # round all float instances to 1 decimal, and replace all NoneType with 0
        if isinstance(average_score, float):
            average_score = round(average_score, 1)
            # print(average_score)
        else:
            average_score = 0
        context['average_score'] = average_score

        # Add 'reviews_number' to context
        # print(Review.objects.filter(entry=entry))
        reviews_number = len(Review.objects.filter(entry=entry))
        # print(reviews_number)
        context['reviews_number'] = reviews_number

        if 'like' in self.request.GET.keys():
            like_type = self.request.GET['like']
            print('Like type: ', like_type)
            # for like creation
            if like_type == 'yes':        
                # check to see if the like already exists
                try:
                    like = Like.objects.get(
                        user=self.request.user,
                        entry=entry,
                    )
                # if the the above look up raises an error
                # it means that the like doesn't exist
                # so we create one;
                except:
                    like = Like.objects.create(
                        user=self.request.user,
                        entry=entry,
                    )
            # for like deletion
            elif like_type == 'no':
                # Only delete the like if it already exists in the database
                try:
                    like = Like.objects.get(
                        user=self.request.user,
                        entry=entry,
                    )
                    like.delete()
                except:
                    print("Like cannot be unliked because it doesn't exist in the database")
        
        # add to context whether or not this entry has been liked by the currently logged in user
        try:
            like = Like.objects.get(
                user=self.request.user,
                entry=entry,
            )
            context['already_liked']='yes'
        except:
            context['already_liked']='no'
        
        
        print(context)

        return context

    context_object_name = "entry"


# Class view

class RequestEntryCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "entries/request_entry_create.html"
    form_class = RequestEntryModelForm

    def get_success_url(self):
        # print(self.object())
        print(self.object.short_url)
        return reverse("entry-fill", kwargs={"short_url": self.object.short_url})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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
        # This is not a normal entry yet, so turn make it False
        entry.normal_entry = False
        entry.save()

        return super(RequestEntryCreateView, self).form_valid(form)


# Class view

class EntryCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "entries/entry_create.html"
    form_class = EntryModelForm

    
    def get_success_url(self):
        # print(self.object())
        print(self.object.short_url)
        return reverse("entry-detail-short-url", kwargs={"short_url": self.object.short_url})

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

# Function based view


def review_create(request, pk):
    entry_object = Entry.objects.get(id=pk)
    form = ReviewModelForm()

    # the user needs to be logged in in order to leave a review
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    # The following if-branch gets executed when the request is of 'POST' format;
    # However, the first time this view function is called is of format 'GET ...';
    if request.method == "POST":
        form = ReviewModelForm(request.POST)
        if form.is_valid():
            print('<< Form is valid >>')
            print('CLEANED DATA ->',form.cleaned_data)
            comment = form.cleaned_data['comment']
            rating = form.cleaned_data['rating']
            user = request.user
            entry = entry_object
            Review.objects.create(
                comment=comment,
                rating=rating,
                user=user,
                entry=entry
            )
            short_url = entry.short_url
            
            return redirect(reverse("entry-detail-short-url", kwargs={"short_url": short_url}))
        else:
            print('<< Form is not valid >>')
            print('CLEANED DATA ->',form.cleaned_data)
            print('FORM ERRORS ->',form.errors)

    reviews_by_current_user = Review.objects.filter(
        entry=entry_object, user=request.user)
    # print(reviews_by_current_user)
    # print(reviews_number)
    # number of reviews left by current user (can't be higher than 1)
    reviews_number = str(len(reviews_by_current_user))

    # Fetch source_domain in order to add to context
    source_domain = url_parser(entry_object.source)

    context = {
        "form": form,
        "entry": entry_object,
        "reviews_number": reviews_number,
        "source_domain": source_domain
    }
    return render(request, "entries/review_create.html", context)

# Class view


class EntryFillView(LoginRequiredMixin, generic.UpdateView):
    template_name = "entries/entry_fill.html"
    queryset = Entry.objects.all()
    form_class = FillEntryModelForm

    def get_success_url(self):
        short_url = self.get_object().short_url
        return reverse("entry-detail-short-url", kwargs={'short_url': short_url})

    def get_object(self, queryset=None):
        short_url = self.kwargs['short_url']
        entry = Entry.objects.get(short_url=short_url)
        return entry

    def form_valid(self, form):
        # Assign the current logged in user to the entry (different to the user that created the request-type entry)
        entry = form.save(commit=False)
        entry.user = self.request.user
        # change normal_entry to True, since it contains all the info now
        entry.normal_entry = True
        # update the time and date of the creation
        entry.date_created = datetime.now()
        entry.save()
        return super(EntryFillView, self).form_valid(form)

# Class view


class EntryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "entries/entry_update.html"
    queryset = Entry.objects.all()
    form_class = EntryModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pass the number of reviews left to this entry via the context
        # so we can restrict updating for entries who have received more than one review;
        entry_object = self.get_object()
        entry_reviews = Review.objects.filter(entry=entry_object)
        entry_reviews_number = len(entry_reviews)
        context['entry_reviews_number'] = entry_reviews_number

        # check to see if the user logged in is also the creator of the entry
        user_logged_in = self.request.user
        user_entry = entry_object.user
        are_users_the_same = user_logged_in == user_entry
        print('Are users the same?', are_users_the_same)
        context['are_users_the_same'] = are_users_the_same
        print(context)
        return context

    def get_success_url(self):
        short_url = self.get_object().short_url
        return reverse("entry-detail-short-url", kwargs={'short_url': short_url})


# Class view
class EntryDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "entries/entry_delete.html"
    queryset = Entry.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # check to see if the user logged in is also the creator of the entry
        entry_object = self.get_object()
        user_logged_in = self.request.user
        user_entry = entry_object.user
        are_users_the_same = user_logged_in == user_entry
        print('Are users the same?', are_users_the_same)
        context['are_users_the_same'] = are_users_the_same
        print(context)
        return context

    def get_success_url(self):
        return reverse("entries:entry-list")


##############################################
############ DEPRECATED CODE #################
##############################################

class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "entries/review_create.html"
    form_class = ReviewModelForm

    def get_success_url(self):
        return reverse("entries:entry-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('CONTEXT ->', context)
        return context

    def form_valid(self, form):
        # Assign the current logged in user to the review
        review = form.save(commit=False)
        review.user = self.request.user
        # Assign the current entry to the review
        print('POST LINE -->', self.request.POST)
        print(review.user)

        print(self)
        review.entry = Entry.objects.get(id=27)

        review.save()
        return super(ReviewCreateView, self).form_valid(form)


# Class View


class MyEntryListByCategoryView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"

    def get_queryset(self):
        entry_user = self.request.user
        category = self.kwargs['category']
        return Entry.objects.filter(user=entry_user, category=category)

    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

# Class view


class MyEntryListView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/entry_list.html"

    # Filter the query set so we only display the entries of the current user
    def get_queryset(self):
        entry_user = self.request.user
        return Entry.objects.filter(user=entry_user)
    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

# Function view


def entry_list(request):
    # Order entries by date_created (the '-' means last added first)
    entries = Entry.objects.all().order_by('-date_created')
    # default value of 'category'
    category = 'all'
    print(request.GET.keys())

    # if 'category' is passed as a '?category=xXx' parameter to the URL
    if 'category' in request.GET.keys():
        category = request.GET['category']
        # if the category is different to 'all' apply another filter to the entries
        if (category != 'all'):
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

# Function view


def entry_delete(request, pk):
    entry = Entry.objects.get(id=pk)
    entry.delete()
    return redirect("/entries")

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

# Function view


def entry_detail(request, pk):
    # Return the entry with id = pk
    entry = Entry.objects.get(id=pk)
    context = {
        "entry": entry
    }
    return render(request, "entries/entry_detail.html", context)

# Function view


def landing_page(request):
    return render(request, "landing.html")

# Class View


class EntryListByCategoryView(LoginRequiredMixin, generic.ListView):
    template_name = "entries/testing.html"

    def get_queryset(self):
        category = self.kwargs['category']
        return Entry.objects.filter(category=category)

    # change the default name for the iterable list from 'object_list' to 'entries'
    context_object_name = "entries"

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
