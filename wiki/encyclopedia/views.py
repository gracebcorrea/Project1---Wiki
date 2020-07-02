from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util




def index(request):
    if "Pwiki" not in request.session:
        request.session["Pwiki"] = []

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        "encyclopedia": request.session["Pwiki"]
    })

def NewPage(request):
    return ("NewPage.html")

def RandomPage(request):
    return ("RandomPage.html")
