from django.contrib import admin
from django.urls import path
from entries.views import home_page

app_name = "entries"

urlpatterns = [
    path('', home_page)
]