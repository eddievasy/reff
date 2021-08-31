from django.contrib import admin
from .models import User, Entry, Review, Like

admin.site.register(User)
admin.site.register(Entry)
admin.site.register(Review)
admin.site.register(Like)
