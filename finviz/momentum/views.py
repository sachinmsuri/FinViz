from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from iexcloud.iexcloud import iexCloud
from json import dumps


# Create your views here.

def momentum(request):
    return render(request, 'momentum.html', {})