from django.contrib import admin
from django.urls import path
from entries.views import entry_list, entry_detail, entry_create, entry_update, entry_delete, review_create, EntryListView, EntryDetailView, EntryCreateView, EntryUpdateView, EntryDeleteView, MyEntryListView, EntryListByCategoryView, MyEntryListByCategoryView, ReviewCreateView, ReviewListView

app_name = "entries"

urlpatterns = [
    # By giving paths names, we can reference the paths across HTML files without worrying
    # about a ripple effect taking place when changing the path URL below.
    path('', EntryListView.as_view(), name='entry-list'),
    path('create/', EntryCreateView.as_view(), name='entry-create'),
    # the path below has been implemented through the entry-list path using '?param=xXx' parameters instead
    # path('mine/', MyEntryListView.as_view(), name='my-entry-list'),
    # the '<>' syntax is used when generating dynamic URLs;
    # it is also recommended to keep the URL paths
    # containing primary keys (<pk>) at the bottom of the list;
    # or the primary key can be declared as <int: pk>
    path('<int:pk>/', EntryDetailView.as_view(), name='entry-detail'),
    path('update-<int:pk>/', EntryUpdateView.as_view(), name='entry-update'),
    path('delete-<int:pk>/', EntryDeleteView.as_view(), name='entry-delete'),
    path('review-<int:pk>/', review_create, name='review-create'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    # the paths below have been implemented through the entry-list path using '?param=xXx' parameters instead
    # path('category-<str:category>/', EntryListByCategoryView.as_view(), name='entry-list-by-category'),
    # path('mine/<str:category>/', MyEntryListByCategoryView.as_view(), name='my-entry-list-by-category')
]
