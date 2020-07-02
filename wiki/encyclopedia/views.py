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

def NewPage(request):
    return ("NewPage.html")

def RandomPage(request):
    return ("RandomPage.html")


#New Files
def add(request):
    if request.method == "POST":
        form = NewentrieForm(request.POST)
        if form.is_valid():
            entrie = form.cleaned_data["entrie"]
            request.session["entries"] += [entrie]
            return HttpResponseRedirect(reverse("entries:index"))
        else:
            return render(request, "entries/add.html", {
                "form": form
            })
    else:
        return render(request, "entries/add.html", {
            "form": NewentrieForm()
        })
