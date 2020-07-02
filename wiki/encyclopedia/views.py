from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewEntrieForm(forms.Form):
    entrie = forms.CharField(label="New Entrie")


def index(request):
    if "Pwiki" not in request.session:
        request.session["Pwiki"] = []

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        "encyclopedia": request.session["Pwiki"]
    })



#New Files
def Entries(request):
    if request.method == "POST":
        form = NewEntrieForm(request.POST)
        if form.is_valid():
            entrie = form.cleaned_data["entry"]
            request.session["entries"] += [entry]
            return HttpResponseRedirect(reverse("entries:index"))
        else:
            return render(request, "entries/{{entry}}.html", {
                "form": form
            })
    else:
        return render(request, "entries/<entry>.html", {
            "form": NewEntrieForm()
        })


def AlertsDjango(request):
    return render(request, "Alerts/AlertsDjango.html")


def NewPage(request):
    return ("NewPage.html")

def RandomPage(request):
    return ("RandomPage.html")


def EntryPage(request):
    return ("EntryPage.html")

def EditPage(request):
    return ("EditPage.html")    
