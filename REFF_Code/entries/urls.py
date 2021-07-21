from django.contrib import admin
from django.urls import path
from entries.views import entry_list, entry_detail, entry_create, entry_update, entry_delete

app_name = "entries"

urlpatterns = [
    # By giving paths names, we can reference the paths across HTML files without worrying
    # about a ripple effect taking place when changing the path URL below.
    path('entries', entry_list, name='entry-list'),
    path('entries/', entry_list),
    path('create/', entry_create, name='entry-create'),
    # the '<>' syntax is used when generating dynamic URLs;
    # it is also recommended to keep the URL paths
    # containing primary keys (<pk>) at the bottom of the list;
    # or the primary key can be declared as <int: pk>
    path('entries/<int:pk>/', entry_detail, name='entry-detail'),
    path('entries/<int:pk>/update/', entry_update, name='entry-update'),
    path('entries/<int:pk>/delete/', entry_delete, name='entry-delete') 
]