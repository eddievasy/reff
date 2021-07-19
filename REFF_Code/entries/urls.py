from django.contrib import admin
from django.urls import path
from entries.views import entry_list, entry_detail, entry_create

app_name = "entries"

urlpatterns = [
    path('entries', entry_list),
    path('entries/', entry_list),
    path('create/', entry_create),
    # the '<>' syntax is used when generating dynamic URLs;
    # it is also recommended to keep the URL paths
    # containing primary keys (<pk>) at the bottom of the list;
    # or the primary key can be declared as <int: pk>
    path('entries/<pk>/', entry_detail),
]