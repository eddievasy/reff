from django.shortcuts import render
from django.http import HttpResponse
from .models import Entry

# Create your views here.
 
def home_page(request):
    
     
    entries = Entry.objects.all()

    context = {
        "entries": entries
    }


    return render(request, "second_page.html", context)
