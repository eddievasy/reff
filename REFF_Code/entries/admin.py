from django.contrib import admin
from .models import User, Entry, Contributor

admin.site.register(User)
admin.site.register(Entry)
admin.site.register(Contributor)