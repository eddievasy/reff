from django.contrib import admin
from django.urls import path
from entries.views import entry_list, entry_detail, entry_create, entry_update, entry_delete, EntryListView, EntryDetailView, EntryCreateView, EntryUpdateView, EntryDeleteView, MyEntryListView

app_name = "entries"

urlpatterns = [
    # By giving paths names, we can reference the paths across HTML files without worrying
    # about a ripple effect taking place when changing the path URL below.
    path('', EntryListView.as_view(), name='entry-list'),
    path('create/', EntryCreateView.as_view(), name='entry-create'),
    path('mine/', MyEntryListView.as_view(), name='my-entry-list'),
    # the '<>' syntax is used when generating dynamic URLs;
    # it is also recommended to keep the URL paths
    # containing primary keys (<pk>) at the bottom of the list;
    # or the primary key can be declared as <int: pk>
    path('<int:pk>/', EntryDetailView.as_view(), name='entry-detail'),
    path('<int:pk>/update/', EntryUpdateView.as_view(), name='entry-update'),
    path('<int:pk>/delete/', EntryDeleteView.as_view() , name='entry-delete') 
] 